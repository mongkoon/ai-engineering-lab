# SageMaker SDK 3.x implementation notes

This project uses SDK **3.26.0**, whose imports and modeling APIs differ from older SageMaker SDK 2.x examples.

| Purpose | SDK 3.x API |
| --- | --- |
| Processing | `sagemaker.core.processing.ScriptProcessor` |
| Processing S3 I/O | `sagemaker.core.shapes.ProcessingInput` / `ProcessingOutput` |
| Pipeline execution context | `sagemaker.core.workflow.pipeline_context.PipelineSession` |
| Pipeline parameters | `sagemaker.core.workflow.parameters.ParameterString` |
| Model training | `sagemaker.train.ModelTrainer` |
| Training configuration | `sagemaker.train.configs.Compute`, `InputData`, `SourceCode`, `OutputDataConfig` |
| Workflow steps | `sagemaker.mlops.workflow.steps.ProcessingStep` / `TrainingStep` |
| Workflow definition | `sagemaker.mlops.workflow.pipeline.Pipeline` |
| Evaluation file descriptor | `sagemaker.core.workflow.properties.PropertyFile` |

## Safe validation sequence

1. Validate the source scripts locally, including the production-style model artifact archive and the `evaluation.json` format.
2. Build a `Pipeline` object and inspect `json.loads(pipeline.definition())`.
3. Check that the definition has exactly three steps and contains `NEstimators`, `ModelType` and `UseScaling`.
4. Verify `Evaluate.PropertyFiles` contains `PropertyFileName: EvalReport`, `OutputName: evaluation`, `FilePath: evaluation.json`.
5. Register with `upsert(role_arn=...)` only after structure checks.
6. Start one execution at a time, verify statuses, and inspect the actual S3 report.

## Warnings observed during setup

- `Popping out ProcessingJobName/TrainingJobName`: SDK removes fixed job names so pipeline execution can assign them dynamically. This is an informational warning during definition serialization.
- `Cannot simulate policies` / `iam:SimulatePrincipalPolicy`: lack of IAM policy simulation permission does not by itself prove that SageMaker Processing/Training permissions are absent. Verify an actual operation and investigate an AccessDenied failure if one occurs.
- `PipelineSession ... No Job being started`: expected when constructing pipeline steps rather than running them interactively.

The AWS pipeline may upload source archives during definition generation. Running `pipeline.definition()` is not equivalent to executing Processing/Training jobs, but it can still write small objects to S3.
