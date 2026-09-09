import tarfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    PROJECT_ROOT
    / "artifacts"
    / "model.joblib"
)

PACKAGE_FILE = (
    PROJECT_ROOT
    / "artifacts"
    / "model.tar.gz"
)


def main():
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            "model.joblib not found. "
            "Run python src/train.py first."
        )

    with tarfile.open(
        PACKAGE_FILE,
        "w:gz",
    ) as archive:
        archive.add(
            MODEL_FILE,
            arcname="model.joblib",
        )

    print(f"Created: {PACKAGE_FILE}")


if __name__ == "__main__":
    main()