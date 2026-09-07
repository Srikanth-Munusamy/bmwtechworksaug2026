from decimal import Decimal

from pydantic import BaseModel, Field


# -------------------------------------------------
# Service Job input
# -------------------------------------------------
class ServiceJobCreate(BaseModel):

    job_id: str

    vehicle_model: str

    issue: str

    part_number: str

    quantity: int = Field(
        gt=0
    )

    priority: str

    status: str = "OPEN"


# -------------------------------------------------
# Supplier Quote input
# -------------------------------------------------
class SupplierQuoteCreate(BaseModel):

    supplier_id: str

    supplier_name: str

    part_number: str

    stock: int = Field(
        ge=0
    )

    unit_price: Decimal = Field(
        gt=0
    )

    delivery_days: int = Field(
        ge=0
    )


# -------------------------------------------------
# Purchase Request input
# -------------------------------------------------
class PurchaseRequestCreate(BaseModel):

    job_id: str

    supplier_id: str

    part_number: str

    quantity: int = Field(
        gt=0
    )

    unit_price: Decimal = Field(
        gt=0
    )