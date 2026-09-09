from pathlib import Path

import boto3

from sagemakermodule.config import (
    AWS_REGION,
    S3_BUCKET,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    PROJECT_ROOT
    / "artifacts"
    / "model.tar.gz"
)

METRICS_FILE = (
    PROJECT_ROOT
    / "artifacts"
    / "metrics.json"
)


def main():
    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION,
    )

    s3.upload_file(
        MODEL_FILE,
        S3_BUCKET,
        "models/parts-demand/v1/model.tar.gz",
    )

    s3.upload_file(
        METRICS_FILE,
        S3_BUCKET,
        "models/parts-demand/v1/metrics.json",
    )

    print("Model uploaded to S3.")


if __name__ == "__main__":
    main()