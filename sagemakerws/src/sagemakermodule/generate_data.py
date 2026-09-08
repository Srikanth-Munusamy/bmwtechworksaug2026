from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIRECTORY = PROJECT_ROOT / "data"
DATA_FILE = DATA_DIRECTORY / "parts_demand.csv"


def generate_dataset(number_of_rows: int = 1000) -> pd.DataFrame:
    rng = np.random.default_rng(42)

    part_category = rng.integers(0, 5, number_of_rows)
    current_stock = rng.integers(20, 500, number_of_rows)
    previous_month_demand = rng.integers(30, 400, number_of_rows)
    average_monthly_demand = rng.integers(40, 350, number_of_rows)
    vehicle_sales = rng.integers(100, 1000, number_of_rows)
    seasonal_index = rng.uniform(0.7, 1.5, number_of_rows).round(2)
    lead_time_days = rng.integers(2, 45, number_of_rows)

    noise = rng.normal(0, 12, number_of_rows)

    next_month_demand = (
        0.35 * previous_month_demand
        + 0.40 * average_monthly_demand
        + 0.08 * vehicle_sales
        + 25 * seasonal_index
        + 0.30 * lead_time_days
        - 0.04 * current_stock
        + 4 * part_category
        + noise
    )

    next_month_demand = np.maximum(
        np.round(next_month_demand),
        0,
    ).astype(int)

    return pd.DataFrame(
        {
            "part_category": part_category,
            "current_stock": current_stock,
            "previous_month_demand": previous_month_demand,
            "average_monthly_demand": average_monthly_demand,
            "vehicle_sales": vehicle_sales,
            "seasonal_index": seasonal_index,
            "lead_time_days": lead_time_days,
            "next_month_demand": next_month_demand,
        }
    )


def main() -> None:
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    dataset = generate_dataset()
    dataset.to_csv(DATA_FILE, index=False)

    print(f"Dataset created: {DATA_FILE}")
    print(f"Rows: {len(dataset)}")
    print(dataset.head())


if __name__ == "__main__":
    main()