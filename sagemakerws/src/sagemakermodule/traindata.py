import tomllib
from pathlib import Path

import boto3
import pandas as pd
import sagemaker
from sagemaker.inputs import TrainingInput
from sagemaker.serializers import CSVSerializer
from sagemaker.deserializers import JSONDeserializer
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIRECTORY = PROJECT_ROOT / "src"
CONFIG_FILE = PROJECT_ROOT / "config.toml"
DATA_FILE = SRC_DIRECTORY / "data" / "parts_demand.csv"
PREPARED_DIRECTORY = SRC_DIRECTORY / "data" / "prepared"

with CONFIG_FILE.open("rb") as file:
    CONFIG = tomllib.load(file)


REGION = CONFIG["aws"]["region"]
BUCKET = CONFIG["aws"]["bucket"]
ROLE = CONFIG["aws"]["execution_role_arn"]

TRAINING_PREFIX = CONFIG["s3"]["training_prefix"]
TESTING_PREFIX = CONFIG["s3"]["testing_prefix"]
MODEL_PREFIX = CONFIG["s3"]["model_prefix"]


def prepare_data() -> tuple[Path, Path]:
    dataset = pd.read_csv(DATA_FILE)

    train_data, test_data = train_test_split(
        dataset,
        test_size=0.20,
        random_state=42,
    )

    PREPARED_DIRECTORY.mkdir(parents=True, exist_ok=True)

    train_file = PREPARED_DIRECTORY / "train.csv"
    test_file = PREPARED_DIRECTORY / "test.csv"

    # SageMaker built-in XGBoost expects the target as the first column.
    column_order = [
        "next_month_demand",
        "part_category",
        "current_stock",
        "previous_month_demand",
        "average_monthly_demand",
        "vehicle_sales",
        "seasonal_index",
        "lead_time_days",
    ]

    train_data[column_order].to_csv(
        train_file,
        index=False,
        header=False,
    )

    test_data[column_order].to_csv(
        test_file,
        index=False,
        header=False,
    )

    return train_file, test_file


def upload_data(
    session: sagemaker.Session,
    train_file: Path,
    test_file: Path,
) -> tuple[str, str]:

    train_uri = session.upload_data(
        path=str(train_file),
        bucket=BUCKET,
        key_prefix=TRAINING_PREFIX,
    )

    test_uri = session.upload_data(
        path=str(test_file),
        bucket=BUCKET,
        key_prefix=TESTING_PREFIX,
    )

    return train_uri, test_uri


def train_model() -> None:
    boto_session = boto3.Session(region_name=REGION)
    sagemaker_session = sagemaker.Session(
        boto_session=boto_session
    )

    train_file, test_file = prepare_data()

    train_uri, test_uri = upload_data(
        sagemaker_session,
        train_file,
        test_file,
    )

    image_uri = sagemaker.image_uris.retrieve(
        framework="xgboost",
        region=REGION,
        version=CONFIG["training"]["framework_version"],
        py_version=CONFIG["training"]["python_version"],
        instance_type=CONFIG["training"]["instance_type"],
    )

    estimator = sagemaker.estimator.Estimator(
        image_uri=image_uri,
        role=ROLE,
        instance_count=CONFIG["training"]["instance_count"],
        instance_type=CONFIG["training"]["instance_type"],
        output_path=f"s3://{BUCKET}/{MODEL_PREFIX}",
        sagemaker_session=sagemaker_session,
    )

    estimator.set_hyperparameters(
        objective="reg:squarederror",
        num_round=150,
        max_depth=5,
        eta=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="rmse",
    )

    training_channels = {
        "train": TrainingInput(
            train_uri,
            content_type="text/csv",
        ),
        "validation": TrainingInput(
            test_uri,
            content_type="text/csv",
        ),
    }

    estimator.fit(training_channels)

    print("Training completed.")
    print(f"Training job: {estimator.latest_training_job.name}")
    print(f"Model artifact: {estimator.model_data}")

    # Save the latest model location for deployment.
    model_location_file = (
        PROJECT_ROOT / "data" / "model_location.txt"
    )

    model_location_file.write_text(
        estimator.model_data,
        encoding="utf-8",
    )


if __name__ == "__main__":
    train_model()