"""Validate the recorded metric reports; preserve original evidence files."""

import csv
import argparse
import json
from pathlib import Path

REPORTS = [
    ("RF-N10", "RandomForest", "OFF", 10),
    ("RF-N50", "RandomForest", "OFF", 50),
    ("RF-N100", "RandomForest", "OFF", 100),
    ("LR-NOSCALE", "LogisticRegression", "OFF", None),
    ("LR-SCALE", "LogisticRegression", "ON", None),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-derived-csv", action="store_true", help="Export a separate CSV; do not overwrite the original")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    result_dir = root / "results"
    rows = []
    for experiment, model, scaling, trees in REPORTS:
        path = result_dir / f"evaluation_{experiment.lower()}.json"
        report = json.loads(path.read_text(encoding="utf-8"))
        assert report["positive_class"] == 0
        assert report["positive_class_name"] == "malignant"
        assert report["test_samples"] == 114
        scores = report["metrics"]
        assert all(k in scores for k in ("accuracy", "precision", "recall", "f1"))
        matrix = report["confusion_matrix"]["matrix"]
        assert sum(map(sum, matrix)) == 114
        assert matrix[0][1] == report["confusion_matrix"]["malignant_false_negatives"]
        rows.append({
            "experiment": experiment,
            "model": model,
            "scaling": scaling,
            "n_estimators": trees if trees is not None else "",
            "accuracy": scores["accuracy"]["value"],
            "precision_malignant": scores["precision"]["value"],
            "recall_malignant": scores["recall"]["value"],
            "f1_malignant": scores["f1"]["value"],
            "malignant_false_negatives": report["confusion_matrix"]["malignant_false_negatives"],
        })
    if args.write_derived_csv:
        target = result_dir / "experiment_comparison_derived.csv"
        with target.open("w", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        print("Derived CSV:", target)
    for record in rows:
        print(record["experiment"], record["accuracy"], record["recall_malignant"])
    print("Result validation: OK")


if __name__ == "__main__":
    main()
