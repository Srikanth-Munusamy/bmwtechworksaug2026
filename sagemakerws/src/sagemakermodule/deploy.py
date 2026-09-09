import boto3
import sagemaker

from sagemaker.sklearn.model import SKLearnModel

from sagemakermodule.config import (
    AWS_REGION,
    ENDPOINT_NAME,
    S3_BUCKET,
    SAGEMAKER_ROLE_ARN,
)


def main():
    boto_session = boto3.Session(
        region_name=AWS_REGION,
    )

    sagemaker_session = sagemaker.Session(
        boto_session=boto_session,
    )

    model_data = (
        f"s3://{S3_BUCKET}/"
        "models/parts-demand/v1/"
        "model.tar.gz"
    )

    model = SKLearnModel(
        model_data=model_data,
        role=SAGEMAKER_ROLE_ARN,
        entry_point="inference.py",
        source_dir="src/sagemakermodule",
        framework_version="1.2-1",
        py_version="py3",
        sagemaker_session=sagemaker_session,
    )

    predictor = model.deploy(
        initial_instance_count=1,
        instance_type="ml.c4.large",
        endpoint_name=ENDPOINT_NAME,
    )

    print(
        f"Endpoint deployed: "
        f"{predictor.endpoint_name}"
    )


if __name__ == "__main__":
    main()