from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIRECTORY = PROJECT_ROOT / "src"
DATA_FILE = SRC_DIRECTORY / "data" / "parts_demand.csv"

PREPARED_DIRECTORY = SRC_DIRECTORY / "data" / "prepared"
MODEL_DIRECTORY = PROJECT_ROOT / "models"

MODEL_FILE = (
    MODEL_DIRECTORY
    / "parts_demand_model.joblib"
)


FEATURE_COLUMNS = [
    "part_category",
    "current_stock",
    "previous_month_demand",
    "average_monthly_demand",
    "vehicle_sales",
    "seasonal_index",
    "lead_time_days",
]

TARGET_COLUMN = "next_month_demand"


def main():
    data = pd.read_csv(DATA_FILE)

    data.columns = (
        data.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print("CSV columns:", data.columns.tolist())

    missing_columns = [
        column
        for column in FEATURE_COLUMNS + [TARGET_COLUMN]
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}. "
            f"Available columns: {data.columns.tolist()}"
        )

    features = data[FEATURE_COLUMNS]

    target = data[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.20,
        random_state=42,
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    MODEL_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        {
            "model": model,
            "feature_columns": FEATURE_COLUMNS,
        },
        MODEL_FILE,
    )

    print(f"Model saved successfully: {MODEL_FILE}")
    print(f"Validation MAE: {mae:.2f}")


if __name__ == "__main__":
    main()