from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "parts_demand_model.joblib"
)


def load_model():
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"Local model not found: {MODEL_FILE}\n"
            "Run this command first:\n"
            "python -m sagemakermodule.train_local"
        )

    return joblib.load(MODEL_FILE)


SAVED_MODEL = load_model()

MODEL = SAVED_MODEL["model"]

FEATURE_COLUMNS = SAVED_MODEL["feature_columns"]


def predict_demand(
    part_category: int,
    current_stock: int,
    previous_month_demand: int,
    average_monthly_demand: int,
    vehicle_sales: int,
    seasonal_index: float,
    lead_time_days: int,
) -> int:
    input_data = pd.DataFrame(
        [
            {
                "part_category": part_category,
                "current_stock": current_stock,
                "previous_month_demand": previous_month_demand,
                "average_monthly_demand": average_monthly_demand,
                "vehicle_sales": vehicle_sales,
                "seasonal_index": seasonal_index,
                "lead_time_days": lead_time_days,
            }
        ],
        columns=FEATURE_COLUMNS,
    )

    prediction = MODEL.predict(input_data)[0]

    return max(0, round(float(prediction)))


if __name__ == "__main__":
    predicted_demand = predict_demand(
        part_category=2,
        current_stock=120,
        previous_month_demand=180,
        average_monthly_demand=160,
        vehicle_sales=450,
        seasonal_index=1.2,
        lead_time_days=14,
    )

    print(f"Predicted next-month demand: {predicted_demand}")