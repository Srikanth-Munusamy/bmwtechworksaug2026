import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "parts_demand.csv"
)

ARTIFACTS_DIRECTORY = (
    PROJECT_ROOT
    / "artifacts"
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

TARGET_COLUMN = "demand"


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"CSV file not found: {DATA_FILE}"
        )

    ARTIFACTS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = pd.read_csv(DATA_FILE)

    data = data.dropna(
        subset=FEATURE_COLUMNS + [TARGET_COLUMN]
    )

    X = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    metrics = {
        "model_version": "v1",
        "algorithm": "RandomForestRegressor",
        "mae": round(
            float(mean_absolute_error(y_test, predictions)),
            2,
        ),
        "rmse": round(
            float(
                mean_squared_error(
                    y_test,
                    predictions,
                ) ** 0.5
            ),
            2,
        ),
        "r2_score": round(
            float(r2_score(y_test, predictions)),
            4,
        ),
        "training_rows": len(X_train),
        "test_rows": len(X_test),
    }

    model_file = (
        ARTIFACTS_DIRECTORY
        / "model.joblib"
    )

    metrics_file = (
        ARTIFACTS_DIRECTORY
        / "metrics.json"
    )

    joblib.dump(model, model_file)

    metrics_file.write_text(
        json.dumps(
            metrics,
            indent=2,
        )
    )

    print("Training completed.")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()