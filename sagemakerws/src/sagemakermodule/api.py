from fastapi import FastAPI
from pydantic import BaseModel, Field

from .predict import predict_demand


app = FastAPI(
    title="BMW Parts Demand API",
    version="1.0.0",
)


class DemandRequest(BaseModel):
    part_category: int = Field(ge=0, le=4)
    current_stock: int = Field(ge=0)
    previous_month_demand: int = Field(ge=0)
    average_monthly_demand: int = Field(ge=0)
    vehicle_sales: int = Field(ge=0)
    seasonal_index: float = Field(gt=0)
    lead_time_days: int = Field(ge=0)


class DemandResponse(BaseModel):
    predicted_demand: int
    reorder_required: bool
    recommended_order_quantity: int


@app.get("/health")
def health() -> dict:
    return {"status": "UP"}


@app.post(
    "/predictions/v1.0",
    response_model=DemandResponse,
)
def create_prediction(
    request: DemandRequest,
) -> DemandResponse:

    prediction = predict_demand(
        part_category=request.part_category,
        current_stock=request.current_stock,
        previous_month_demand=request.previous_month_demand,
        average_monthly_demand=request.average_monthly_demand,
        vehicle_sales=request.vehicle_sales,
        seasonal_index=request.seasonal_index,
        lead_time_days=request.lead_time_days,
    )

    recommended_quantity = max(
        prediction - request.current_stock,
        0,
    )

    return DemandResponse(
        predicted_demand=prediction,
        reorder_required=recommended_quantity > 0,
        recommended_order_quantity=recommended_quantity,
    )