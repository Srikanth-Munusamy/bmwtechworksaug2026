from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import mapped_column

from backend.database import Base


class ServiceJob(Base):
    __tablename__ = "service_jobs"

    job_id = mapped_column(
        String(20),
        primary_key=True
    )

    vehicle_model = mapped_column(
        String(100),
        nullable=False
    )

    issue = mapped_column(
        String(200),
        nullable=False
    )

    part_number = mapped_column(
        String(30),
        nullable=False
    )

    quantity = mapped_column(
        Integer,
        nullable=False
    )

    priority = mapped_column(
        String(20),
        nullable=False
    )

    status = mapped_column(
        String(30),
        default="OPEN"
    )


class SupplierQuote(Base):
    __tablename__ = "supplier_quotes"

    id = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    supplier_id = mapped_column(
        String(20),
        nullable=False
    )

    supplier_name = mapped_column(
        String(100),
        nullable=False
    )

    part_number = mapped_column(
        String(30),
        nullable=False
    )

    stock = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    unit_price = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    delivery_days = mapped_column(
        Integer,
        nullable=False,
        default=0
    )


class PurchaseRequest(Base):
    __tablename__ = "purchase_requests"

    pr_id = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    job_id = mapped_column(
        String(20),
        nullable=False
    )

    supplier_id = mapped_column(
        String(20),
        nullable=False
    )

    part_number = mapped_column(
        String(30),
        nullable=False
    )

    quantity = mapped_column(
        Integer,
        nullable=False
    )

    unit_price = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    total_price = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    status = mapped_column(
        String(30),
        default="CREATED"
    )