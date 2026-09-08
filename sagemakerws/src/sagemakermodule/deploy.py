from pathlib import Path

import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "parts_demand_model.joblib"
)


def deploy_model() -> None:
    """
    Local deployment means loading the trained model.
    FastAPI will use this same model file for predictions.
    """

    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"Local model file not found:\n{MODEL_FILE}\n\n"
            "First run:\n"
            "python -m sagemakermodule.train_local"
        )

    saved_model = joblib.load(MODEL_FILE)

    model = saved_model["model"]
    feature_columns = saved_model["feature_columns"]

    print("Local model loaded successfully.")
    print(f"Model type: {type(model).__name__}")
    print(f"Model path: {MODEL_FILE}")
    print(f"Features: {feature_columns}")
    print("\nStart FastAPI to serve predictions:")
    print("uvicorn sagemakermodule.api:app --reload --port 8000")


if __name__ == "__main__":
    deploy_model()