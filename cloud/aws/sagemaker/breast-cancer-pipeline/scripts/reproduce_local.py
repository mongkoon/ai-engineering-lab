"""Run all five experiment configurations locally without calling AWS.

Outputs live under a temporary directory, and the recorded SageMaker results
are never modified. This is a functional reproduction check, not proof of
bitwise equivalence across scikit-learn and container versions.
"""

import json
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIGS = [
    ("RF-N10", "random_forest", "false", 10),
    ("RF-N50", "random_forest", "false", 50),
    ("RF-N100", "random_forest", "false", 100),
    ("LR-NOSCALE", "logistic_regression", "false", 10),
    ("LR-SCALE", "logistic_regression", "true", 10),
]


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="bc-local-") as temporary:
        base = Path(temporary)
        (base / "input").mkdir()
        (base / "input" / "breast_cancer.csv").write_bytes(
            (ROOT / "data" / "breast_cancer.csv").read_bytes()
        )
        subprocess.run(
            [sys.executable, str(ROOT / "src/preprocess.py")],
            env={**os.environ, "PROCESSING_BASE": str(base)},
            check=True,
            capture_output=True,
            text=True,
        )

        print("Local reproduction | same data split | class 0 = malignant")
        print("Run          Accuracy Precision Recall    F1       FN  Recorded accuracy")
        for label, model, scaling, trees in CONFIGS:
            run_base = base / label
            for subdir in ("model", "test", "evaluation"):
                (run_base / subdir).mkdir(parents=True)
            (run_base / "test" / "test.csv").write_bytes(
                (base / "test" / "test.csv").read_bytes()
            )
            subprocess.run(
                [sys.executable, str(ROOT / "src/train_multi.py"),
                 "--model_type", model,
                 "--use_scaling", scaling,
                 "--n_estimators", str(trees),
                 "--random_state", "42"],
                check=True, capture_output=True, text=True,
                env={
                    **os.environ,
                    "SM_CHANNEL_TRAIN": str(base / "train"),
                    "SM_MODEL_DIR": str(run_base / "model"),
                },
            )
            with tarfile.open(run_base / "model" / "model.tar.gz", "w:gz") as archive:
                archive.add(run_base / "model" / "model.joblib", arcname="model.joblib")
            subprocess.run(
                [sys.executable, str(ROOT / "src/evaluate.py")],
                check=True, capture_output=True, text=True,
                env={**os.environ, "PROCESSING_BASE": str(run_base)},
            )
            local = json.loads((run_base / "evaluation" / "evaluation.json").read_text())
            recorded = json.loads((ROOT / "results" / f"evaluation_{label.lower()}.json").read_text())
            numbers = [local["metrics"][key]["value"] for key in
                       ("accuracy", "precision", "recall", "f1")]
            print(f"{label:<12} " + " ".join(f"{v:.4f}" for v in numbers)
                  + f"  {local['confusion_matrix']['malignant_false_negatives']:>2}"
                  + f"      {recorded['metrics']['accuracy']['value']:.4f}")
        print("Completed five local configurations; recorded cloud reports preserved")


if __name__ == "__main__":
    main()
