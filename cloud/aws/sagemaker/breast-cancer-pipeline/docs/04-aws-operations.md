# AWS operations and resource lifecycle

## Services and resources used

- SageMaker Studio JupyterLab for development
- SageMaker Pipelines with Processing and Training steps
- S3 bucket for raw CSV, script artifacts, model outputs and per-execution `evaluation.json`
- CloudWatch logs and SageMaker pipeline execution history for troubleshooting
- No inference Endpoint was deployed in the experiment

## Verified stop / deployment status

At the end of the recorded evaluation session, SageMaker Studio displayed **no running instances** and the Endpoints list displayed **no endpoints**. These observations do not establish that all storage and metadata resources were deleted or that all AWS charges have ceased.

## Cleanup inventory

For an isolated experiment, first preserve the code and metrics outside AWS and verify no training or processing jobs remain active. Then review resources associated **only with the experiment**:

1. JupyterLab application status, Space and attached EBS storage
2. Experiment-specific SageMaker Pipeline and historical executions
3. S3 objects and experiment-specific bucket
4. Dedicated SageMaker Studio Domain (when created solely for the experiment), associated user profiles/apps, and residual EFS storage
5. Experiment-specific IAM execution role and policies, after ensuring no other workloads depend on them
6. CloudWatch logs and other retained monitoring resources
7. AWS Billing / Cost Explorer for residual storage and usage charges

Deleting a Space or Domain may destroy data. Stop compute first, verify backups, and carefully distinguish unrelated resources. No cleanup command is automated in this repository.

## Safety controls

- `scripts/upsert_pipeline.py` only modifies the AWS Pipeline when given `--apply`.
- `scripts/launch_experiment.py` requires `--execute` and launches **one** execution at a time.
- There is no endpoint creation code.
- Cloud account identifiers, role ARNs, user display names and raw evidence screenshots are deliberately excluded from the public repository.
