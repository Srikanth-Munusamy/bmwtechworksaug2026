import json
from pathlib import Path

from langchain.tools import tool


# -------------------------------------------------
# Paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

VEHICLE_FILE = PROJECT_ROOT / "vehicles.json"


# -------------------------------------------------
# Load vehicle data
# -------------------------------------------------

with open(
    VEHICLE_FILE,
    "r",
    encoding="utf-8"
) as file:

    vehicle_data = json.load(file)


# -------------------------------------------------
# LangChain Tool
# -------------------------------------------------

@tool
def get_vehicle_status(vehicle_id: str) -> dict:
    """
    Get BMW vehicle status using vehicle ID.

    Returns vehicle model, battery level,
    temperature, fault code and status.
    """

    print(
        f"LangChain Tool called: "
        f"get_vehicle_status({vehicle_id})"
    )

    vehicle = vehicle_data.get(
        vehicle_id.upper()
    )

    if vehicle is None:

        return {
            "error": "Vehicle not found"
        }

    return vehicle