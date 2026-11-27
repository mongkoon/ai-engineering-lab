import argparse
import os
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def main():
    parser = argparse.ArgumentParser()

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

    # SageMaker Training 환경 변수
    train_dir = Path(
        os.environ.get("SM_CHANNEL_TRAIN", "/opt/ml/input/data/train")
    )
    model_dir = Path(
        os.environ.get("SM_MODEL_DIR", "/opt/ml/model")
    )

    # 학습 데이터 로드
    df = pd.read_csv(train_dir / "train.csv")

    X = df.drop(columns=["target"])
    y = df["target"]

    # Random Forest 모델 정의
    model = RandomForestClassifier(
        n_estimators=args.n_estimators,
        random_state=args.random_state,
        n_jobs=-1,
    )

    # 모델 학습
    model.fit(X, y)

    # 모델 아티팩트 저장
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / "model.joblib"

    joblib.dump(model, model_path)

    print("=== Training Completed ===")
    print("Training samples:", len(df))
    print("Number of features:", X.shape[1])
    print("n_estimators:", args.n_estimators)
    print("random_state:", args.random_state)
    print("Model saved:", model_path)


if __name__ == "__main__":
    main()
