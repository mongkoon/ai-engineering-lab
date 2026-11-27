"""Export sklearn Breast Cancer Wisconsin (Diagnostic) data to CSV.

Optionally upload the CSV to the exact S3 prefix expected by the pipeline.
No upload occurs unless --upload is provided.
"""

import argparse
import os
from pathlib import Path

from sklearn.datasets import load_breast_cancer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/breast_cancer.csv")
    parser.add_argument("--upload", action="store_true", help="Explicitly upload to S3")
    parser.add_argument("--prefix", default="breast-cancer-pipeline")
    args = parser.parse_args()

    data = load_breast_cancer(as_frame=True).frame
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path, index=False)
    print(f"Dataset: {data.shape[0]} rows, {data.shape[1] - 1} features")
    print(f"Target counts: {data['target'].value_counts().sort_index().to_dict()}")
    print(f"CSV saved: {path}")

    if args.upload:
        import boto3

        bucket = os.environ.get("BC_S3_BUCKET")
        if not bucket:
            raise SystemExit("Set BC_S3_BUCKET before using --upload")
        key = f"{args.prefix}/input/breast_cancer.csv"
        boto3.client("s3").upload_file(str(path), bucket, key)
        print(f"Uploaded: s3://{bucket}/{key}")


if __name__ == "__main__":
    main()
