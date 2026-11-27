"""Build, inspect and optionally register a SageMaker Pipeline.

Use --apply to write the definition to AWS. No job is started by this script.
Run from this project's root directory.
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Allow running this script directly from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.sagemaker_pipeline import build_pipeline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Register/update in AWS")
    parser.add_argument("--region", default=os.getenv("AWS_REGION", "ap-northeast-2"))
    args = parser.parse_args()
    bucket = os.environ.get("BC_S3_BUCKET")
    role = os.environ.get("BC_SAGEMAKER_ROLE_ARN")
    if not bucket or not role:
        raise SystemExit("Set BC_S3_BUCKET and BC_SAGEMAKER_ROLE_ARN first")

    pipeline = build_pipeline(bucket=bucket, role=role, region=args.region)
    definition = json.loads(pipeline.definition())
    steps = definition["Steps"]
    parameters = [p["Name"] for p in definition["Parameters"]]
    assert [s["Name"] for s in steps] == ["Preprocess", "Train", "Evaluate"]
    assert set(parameters) == {"NEstimators", "ModelType", "UseScaling"}
    eval_step = next(s for s in steps if s["Name"] == "Evaluate")
    assert any(
        f.get("PropertyFileName") == "EvalReport"
        and f.get("OutputName") == "evaluation"
        and f.get("FilePath") == "evaluation.json"
        for f in eval_step.get("PropertyFiles", [])
    )

    print("Pipeline:", pipeline.name)
    print("Steps:", [s["Name"] for s in steps])
    print("Parameters:", parameters)
    print("PropertyFile validation: OK")

    if args.apply:
        pipeline.upsert(role_arn=role)
        print("Pipeline definition registered in AWS; no execution started")
    else:
        print("Definition only: add --apply to register (code artifacts may be uploaded to S3)")


if __name__ == "__main__":
    main()
