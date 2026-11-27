import argparse
import os
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# 1. Training parameters
parser = argparse.ArgumentParser()

parser.add_argument(
    "--model_type",
    type=str,
    choices=["random_forest", "logistic_regression"],
    default="random_forest",
)

parser.add_argument(
    "--use_scaling",
    type=str,
    choices=["true", "false"],
    default="false",
)

parser.add_argument(
    "--n_estimators",
    type=int,
    default=100,
)

parser.add_argument(
    "--random_state",
    type=int,
    default=42,
)

args = parser.parse_args()


# 2. SageMaker input/output paths
train_dir = Path(
    os.environ.get(
        "SM_CHANNEL_TRAIN",
        "/opt/ml/input/data/train",
    )
)

model_dir = Path(
    os.environ.get(
        "SM_MODEL_DIR",
        "/opt/ml/model",
    )
)

model_dir.mkdir(parents=True, exist_ok=True)


# 3. Load training data
df = pd.read_csv(train_dir / "train.csv")

X = df.drop(columns=["target"])
y = df["target"]


# 4. Select estimator
if args.model_type == "random_forest":
    estimator = RandomForestClassifier(
        n_estimators=args.n_estimators,
        random_state=args.random_state,
        n_jobs=-1,
    )

else:
    estimator = LogisticRegression(
        max_iter=2000,
        random_state=args.random_state,
    )


# 5. Optional feature scaling
if args.use_scaling == "true":
    model = make_pipeline(
        StandardScaler(),
        estimator,
    )
else:
    model = estimator


# 6. Train model
model.fit(X, y)


# 7. Save model
model_path = model_dir / "model.joblib"
joblib.dump(model, model_path)


# 8. Training summary
print("=== Multi-Model Training ===")
print("Model type:", args.model_type)
print("Use scaling:", args.use_scaling)
print("N estimators:", args.n_estimators)
print("Random state:", args.random_state)
print("Training samples:", len(X))
print("Features:", X.shape[1])
print("Model saved:", model_path)
print("Training script: OK")
