# Reproducibility and local validation

## Proven setup

| Setting | Value |
| --- | --- |
| AWS Region | `ap-northeast-2` |
| SageMaker Python SDK | `sagemaker[train,mlops]==3.26.0` |
| Training and Processing image | `sagemaker-scikit-learn:1.4-2-cpu-py3` |
| Original AWS managed job type | `ml.m5.large` |
| Raw dataset | 569 rows, 30 features + target |
| Data split | 80/20, `stratify=target`, `random_state=42` |
| Model seed | `random_state=42` |
| Malignant class | `target=0`, `pos_label=0` |

The recorded five-run metrics were produced in the original AWS environment. Exact reproducibility across different scikit-learn or container versions is not guaranteed by the seed alone.

## Local execution

From the project root:

```bash
python -m pip install -r requirements.txt
python scripts/prepare_dataset.py
python -m unittest discover -s tests -v
python scripts/inspect_results.py
python scripts/reproduce_local.py
```

No AWS account is required for these commands. Tests exercise stratified preprocessing, both model families, scaler ON/OFF, model archive loading and creation of all four evaluation metrics.

## AWS definition and run lifecycle

First configure the environment with values belonging to your own AWS account. Do not commit them:

```bash
python -m pip install -r requirements-sagemaker.txt
export AWS_REGION=ap-northeast-2
export BC_S3_BUCKET=<your-bucket>
export BC_SAGEMAKER_ROLE_ARN=<your-role-arn>
python scripts/prepare_dataset.py --upload
python scripts/upsert_pipeline.py             # Validate the definition
python scripts/upsert_pipeline.py --apply     # Register/update, no job starts
```

A **single** optional training run can be started with an explicit flag:

```bash
python scripts/launch_experiment.py \
  --model logistic_regression --scaling true --trees 10 \
  --name lr-scaled-demo --execute
```

**AWS charges apply to Processing, Training and JupyterLab resources.** Avoid rerunning an execution command just to inspect status. Use the console or `boto3.describe_pipeline_execution()` / `list_pipeline_execution_steps()` instead.

## Reconstructing the five-run experiment matrix

| Run | `ModelType` | `UseScaling` | `NEstimators` |
| --- | --- | --- | ---: |
| RF-N10 | `random_forest` | `false` | 10 |
| RF-N50 | `random_forest` | `false` | 50 |
| RF-N100 | `random_forest` | `false` | 100 |
| LR-NOSCALE | `logistic_regression` | `false` | 10 (unused) |
| LR-SCALE | `logistic_regression` | `true` | 10 (unused) |

## Repository artifact provenance

Public source files and clean notebooks were organized from the implemented workflow and verified outputs. The original private, executed JupyterLab notebook was **not available as file bytes when this bundle was assembled**. Consequently, these notebooks are reproducible sanitized reconstructions, not verbatim exports of the original execution history. The five evaluation JSON files reproduce the recorded values shown in the AWS S3 evidence; the bundle does not contain original cloud account identifiers or URLs.
