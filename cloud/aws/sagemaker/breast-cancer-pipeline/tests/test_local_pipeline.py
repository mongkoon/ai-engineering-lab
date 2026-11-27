"""Offline functional checks for processing, model artifacts and evaluation.

Run with: python -m unittest discover -s tests -v
No AWS resources or network calls are used.
"""

import json
import os
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent


class LocalPipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.base = Path(cls.temp.name)
        (cls.base / "input").mkdir()
        (cls.base / "input" / "breast_cancer.csv").write_bytes(
            (ROOT / "data" / "breast_cancer.csv").read_bytes()
        )
        env = {**os.environ, "PROCESSING_BASE": str(cls.base)}
        subprocess.run(
            [sys.executable, str(ROOT / "src/preprocess.py")],
            check=True, env=env, capture_output=True, text=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_stratified_split_and_fixed_seed(self):
        train = pd.read_csv(self.base / "train" / "train.csv")
        test = pd.read_csv(self.base / "test" / "test.csv")
        self.assertEqual(len(train), 455)
        self.assertEqual(len(test), 114)
        self.assertEqual(train.target.value_counts().sort_index().to_dict(), {0: 170, 1: 285})
        self.assertEqual(test.target.value_counts().sort_index().to_dict(), {0: 42, 1: 72})

    def _run_model(self, model: str, scaling: str, trees: int = 10) -> dict:
        with tempfile.TemporaryDirectory() as work:
            base = Path(work)
            (base / "model").mkdir()
            (base / "test").mkdir()
            (base / "evaluation").mkdir()
            (base / "test" / "test.csv").write_bytes(
                (self.base / "test" / "test.csv").read_bytes()
            )
            train_env = {
                **os.environ,
                "SM_CHANNEL_TRAIN": str(self.base / "train"),
                "SM_MODEL_DIR": str(base / "model"),
            }
            subprocess.run(
                [sys.executable, str(ROOT / "src/train_multi.py"),
                 "--model_type", model, "--use_scaling", scaling,
                 "--n_estimators", str(trees), "--random_state", "42"],
                check=True, env=train_env, capture_output=True, text=True,
            )
            with tarfile.open(base / "model" / "model.tar.gz", "w:gz") as f:
                f.add(base / "model" / "model.joblib", arcname="model.joblib")
            subprocess.run(
                [sys.executable, str(ROOT / "src/evaluate.py")],
                check=True,
                env={**os.environ, "PROCESSING_BASE": str(base)},
                capture_output=True, text=True,
            )
            return json.loads((base / "evaluation" / "evaluation.json").read_text())

    def test_random_forest_model_and_evaluation_json(self):
        report = self._run_model("random_forest", "false", trees=10)
        self.assertEqual(report["positive_class"], 0)
        self.assertEqual(report["test_samples"], 114)
        self.assertEqual(set(report["metrics"]), {"accuracy", "precision", "recall", "f1"})
        self.assertEqual(sum(map(sum, report["confusion_matrix"]["matrix"])), 114)

    def test_logistic_scaling_options(self):
        no_scaling = self._run_model("logistic_regression", "false")
        with_scaling = self._run_model("logistic_regression", "true")
        for report in (no_scaling, with_scaling):
            self.assertEqual(report["positive_class"], 0)
            self.assertEqual(report["test_samples"], 114)
            self.assertEqual(report["confusion_matrix"]["labels"], [0, 1])
            self.assertIn("recall", report["metrics"])
        self.assertNotEqual(
            no_scaling["confusion_matrix"]["matrix"],
            with_scaling["confusion_matrix"]["matrix"],
        )


if __name__ == "__main__":
    unittest.main()
