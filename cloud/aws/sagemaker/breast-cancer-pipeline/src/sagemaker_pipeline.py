"""SageMaker SDK 3.x Pipeline definition: Preprocess -> Train -> Evaluate.

Requires ``sagemaker[train,mlops]==3.26.0`` and an AWS-authenticated environment.
No managed jobs are started when this function builds the definition.
"""


def build_pipeline(
    *,
    bucket: str,
    role: str,
    region: str = "ap-northeast-2",
    prefix: str = "breast-cancer-pipeline",
    pipeline_name: str = "breast-cancer-ml-pipeline",
    instance_type: str = "ml.m5.large",
    framework_version: str = "1.4-2",
):
    """Construct a registered-ready Pipeline without calling upsert/start."""
    if not bucket or not role:
        raise ValueError("Both bucket and SageMaker execution role are required")

    import boto3
    from sagemaker.core import image_uris
    from sagemaker.core.processing import ScriptProcessor
    from sagemaker.core.shapes import (
        ProcessingInput, ProcessingOutput, ProcessingS3Input, ProcessingS3Output,
    )
    from sagemaker.core.workflow.execution_variables import ExecutionVariables
    from sagemaker.core.workflow.functions import Join
    from sagemaker.core.workflow.parameters import ParameterString
    from sagemaker.core.workflow.pipeline_context import PipelineSession
    from sagemaker.core.workflow.properties import PropertyFile
    from sagemaker.mlops.workflow.pipeline import Pipeline
    from sagemaker.mlops.workflow.steps import ProcessingStep, TrainingStep
    from sagemaker.train import ModelTrainer
    from sagemaker.train.configs import Compute, InputData, OutputDataConfig, SourceCode

    boto_session = boto3.Session(region_name=region)
    pipeline_session = PipelineSession(boto_session=boto_session, default_bucket=bucket)
    sklearn_image = image_uris.retrieve(
        framework="sklearn", region=region, version=framework_version,
        py_version="py3", instance_type=instance_type,
    )
    processor = ScriptProcessor(
        image_uri=sklearn_image,
        command=["python3"],
        role=role,
        instance_type=instance_type,
        instance_count=1,
        max_runtime_in_seconds=900,
        sagemaker_session=pipeline_session,
    )

    def run_s3_path(step: str, output: str | None = None):
        parts = [
            f"s3://{bucket}/{prefix}/runs",
            ExecutionVariables.PIPELINE_EXECUTION_ID,
            step,
        ]
        if output:
            parts.append(output)
        return Join(on="/", values=parts)

    preprocess_args = processor.run(
        code="src/preprocess.py",
        inputs=[
            ProcessingInput(
                input_name="breast-cancer-input",
                s3_input=ProcessingS3Input(
                    s3_uri=f"s3://{bucket}/{prefix}/input/breast_cancer.csv",
                    local_path="/opt/ml/processing/input",
                    s3_data_type="S3Prefix",
                    s3_input_mode="File",
                ),
            )
        ],
        outputs=[
            ProcessingOutput(
                output_name=split,
                s3_output=ProcessingS3Output(
                    s3_uri=run_s3_path("preprocess", split),
                    local_path=f"/opt/ml/processing/{split}",
                    s3_upload_mode="EndOfJob",
                ),
            )
            for split in ("train", "test")
        ],
    )
    step_prep = ProcessingStep(name="Preprocess", step_args=preprocess_args)

    n_estimators = ParameterString(name="NEstimators", default_value="10")
    model_type = ParameterString(name="ModelType", default_value="random_forest")
    use_scaling = ParameterString(name="UseScaling", default_value="false")

    train_s3_uri = (
        step_prep.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri
    )
    trainer = ModelTrainer(
        training_image=sklearn_image,
        source_code=SourceCode(source_dir="src", entry_script="train_multi.py"),
        role=role,
        compute=Compute(instance_type=instance_type, instance_count=1),
        hyperparameters={
            "model_type": model_type,
            "use_scaling": use_scaling,
            "n_estimators": n_estimators,
            "random_state": "42",
        },
        input_data_config=[
            InputData(
                channel_name="train",
                data_source=train_s3_uri,
                content_type="text/csv",
            )
        ],
        output_data_config=OutputDataConfig(
            s3_output_path=f"s3://{bucket}/{prefix}/training"
        ),
        sagemaker_session=pipeline_session,
    )
    step_train = TrainingStep(name="Train", step_args=trainer.train())

    evaluation_property = PropertyFile(
        name="EvalReport", output_name="evaluation", path="evaluation.json"
    )
    model_s3_uri = step_train.properties.ModelArtifacts.S3ModelArtifacts
    test_s3_uri = (
        step_prep.properties.ProcessingOutputConfig.Outputs["test"].S3Output.S3Uri
    )
    evaluation_args = processor.run(
        code="src/evaluate.py",
        inputs=[
            ProcessingInput(
                input_name="model",
                s3_input=ProcessingS3Input(
                    s3_uri=model_s3_uri,
                    local_path="/opt/ml/processing/model",
                    s3_data_type="S3Prefix",
                    s3_input_mode="File",
                ),
            ),
            ProcessingInput(
                input_name="test",
                s3_input=ProcessingS3Input(
                    s3_uri=test_s3_uri,
                    local_path="/opt/ml/processing/test",
                    s3_data_type="S3Prefix",
                    s3_input_mode="File",
                ),
            ),
        ],
        outputs=[
            ProcessingOutput(
                output_name="evaluation",
                s3_output=ProcessingS3Output(
                    s3_uri=run_s3_path("evaluate"),
                    local_path="/opt/ml/processing/evaluation",
                    s3_upload_mode="EndOfJob",
                ),
            )
        ],
    )
    step_eval = ProcessingStep(
        name="Evaluate",
        step_args=evaluation_args,
        property_files=[evaluation_property],
    )
    return Pipeline(
        name=pipeline_name,
        parameters=[n_estimators, model_type, use_scaling],
        steps=[step_prep, step_train, step_eval],
        sagemaker_session=pipeline_session,
    )
