from pathlib import Path

import os
import pandas as pd
from sklearn.model_selection import train_test_split

BASE = Path(
    os.environ.get("PROCESSING_BASE", "/opt/ml/processing")
)
INPUT_PATH = BASE / "input" / "breast_cancer.csv"

# Load dataset
df = pd.read_csv(INPUT_PATH)

if "target" not in df.columns:
    raise ValueError("Missing target column")

# 0 = malignant, 1 = benign
print("Total samples:", len(df))
print("Class distribution:")
print(df["target"].value_counts().sort_index())

# Stratified 80:20 split
train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["target"],
)

# Save outputs for downstream pipeline steps
for folder, data, filename in [
    ("train", train_df, "train.csv"),
    ("test", test_df, "test.csv"),
]:
    output_dir = BASE / folder
    output_dir.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_dir / filename, index=False)

print("Train samples:", len(train_df))
print("Test samples:", len(test_df))
print("Preprocessing completed")
