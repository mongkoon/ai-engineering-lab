import json
import os
import tarfile
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

BASE = Path(
    os.environ.get("PROCESSING_BASE", "/opt/ml/processing")
)

model_archive = BASE / "model" / "model.tar.gz"
test_path = BASE / "test" / "test.csv"
output_dir = BASE / "evaluation"

# Load the model produced by our own training job.
# Do not load model artifacts from untrusted sources.
with tarfile.open(model_archive, "r:gz") as tar:
    member = tar.getmember("model.joblib")

    if not member.isfile():
        raise ValueError("model.joblib is not a regular file")

    model_file = tar.extractfile(member)

    if model_file is None:
        raise ValueError("Cannot read model.joblib")

    model = joblib.load(model_file)

# Load test dataset
df = pd.read_csv(test_path)
X_test = df.drop(columns=["target"])
y_test = df["target"]

# Generate predictions
y_pred = model.predict(X_test)

# Malignant = 0, Benign = 1
POS_LABEL = 0

accuracy = float(accuracy_score(y_test, y_pred))
precision = float(
    precision_score(y_test, y_pred, pos_label=POS_LABEL, zero_division=0)
)
recall = float(
    recall_score(y_test, y_pred, pos_label=POS_LABEL, zero_division=0)
)
f1 = float(
    f1_score(y_test, y_pred, pos_label=POS_LABEL, zero_division=0)
)

cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

report = {
    "positive_class": 0,
    "positive_class_name": "malignant",
    "test_samples": int(len(df)),
    "metrics": {
        "accuracy": {"value": accuracy},
        "precision": {"value": precision},
        "recall": {"value": recall},
        "f1": {"value": f1},
    },
    "confusion_matrix": {
        "labels": [0, 1],
        "matrix": cm.tolist(),
        "malignant_false_negatives": int(cm[0, 1]),
    },
}

# Save evaluation report
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "evaluation.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print("=== Evaluation Completed ===")
print("Test samples:", len(df))
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1-score : {f1:.4f}")
print("Confusion matrix [0, 1]:")
print(cm)
print("Malignant false negatives:", int(cm[0, 1]))
print("Evaluation report:", output_path)
