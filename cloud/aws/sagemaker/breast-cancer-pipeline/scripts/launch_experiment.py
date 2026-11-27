"""Launch exactly one SageMaker Pipeline execution after explicit opt-in.

Run from the project root. SageMaker Processing/Training charges may apply.
No identifier is hard-coded; choose an execution display name at runtime.
"""

import argparse
import os

import boto3


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Start a billable run")
    parser.add_argument("--pipeline", default="breast-cancer-ml-pipeline")
    parser.add_argument("--model", required=True, choices=["random_forest", "logistic_regression"])
    parser.add_argument("--scaling", choices=["true", "false"], default="false")
    parser.add_argument("--trees", type=int, default=10)
    parser.add_argument("--name", required=True, help="Execution display name")
    parser.add_argument("--region", default=os.getenv("AWS_REGION", "ap-northeast-2"))
    args = parser.parse_args()

    if args.trees < 1:
        parser.error("--trees must be a positive integer")
    if not args.execute:
        print("Dry run. No AWS execution has been started.")
        print("Model:", args.model, "Scaling:", args.scaling, "Trees:", args.trees)
        print("Add --execute to start one billable execution")
        return

    client = boto3.client("sagemaker", region_name=args.region)
    response = client.start_pipeline_execution(
        PipelineName=args.pipeline,
        PipelineExecutionDisplayName=args.name,
        PipelineParameters=[
            {"Name": "NEstimators", "Value": str(args.trees)},
            {"Name": "ModelType", "Value": args.model},
            {"Name": "UseScaling", "Value": args.scaling},
        ],
    )
    print("Started exactly one Pipeline execution:", response["PipelineExecutionArn"])


if __name__ == "__main__":
    main()
