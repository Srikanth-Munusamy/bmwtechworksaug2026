from contextlib import asynccontextmanager
from decimal import Decimal

from fastapi import FastAPI, HTTPException
from sqlalchemy import select

from .database import Base, engine, SessionLocal
from .models import (
    ServiceJob,
    SupplierQuote,
    PurchaseRequest
)
from .schemas import (
    ServiceJobCreate,
    SupplierQuoteCreate,
    PurchaseRequestCreate
)


# -------------------------------------------------
# Startup
# -------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Registered SQLAlchemy tables:")
    print(list(Base.metadata.tables.keys()))

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "Database tables created/verified."
    )

    yield


app = FastAPI(
    title="Parts Agent Backend API",
    version="1.0.0",
    lifespan=lifespan
)


# -------------------------------------------------
# Root
# -------------------------------------------------
@app.get("/")
def root():

    return {
        "message":
        "Parts Agent Backend API running"
    }


# -------------------------------------------------
# Health
# -------------------------------------------------
@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =================================================
# SERVICE JOB APIs
# =================================================

@app.post("/service-jobs")
def create_service_job(
    payload: ServiceJobCreate
):

    with SessionLocal() as session:

        existing = session.get(
            ServiceJob,
            payload.job_id
        )

        if existing:

            raise HTTPException(
                status_code=409,
                detail="Job ID already exists"
            )

        row = ServiceJob(
            **payload.model_dump()
        )

        session.add(row)
        session.commit()
        session.refresh(row)

        return {
            "job_id": row.job_id,
            "status": row.status
        }


@app.get("/service-jobs/{job_id}")
def get_service_job(
    job_id: str
):

    with SessionLocal() as session:

        row = session.get(
            ServiceJob,
            job_id
        )

        if row is None:

            raise HTTPException(
                status_code=404,
                detail="Service job not found"
            )

        return {
            "job_id": row.job_id,
            "vehicle_model":
                row.vehicle_model,
            "issue": row.issue,
            "part_number":
                row.part_number,
            "quantity": row.quantity,
            "priority": row.priority,
            "status": row.status
        }


# =================================================
# SUPPLIER APIs
# =================================================

@app.post("/supplier-quotes")
def create_supplier_quote(
    payload: SupplierQuoteCreate
):

    with SessionLocal() as session:

        row = SupplierQuote(
            **payload.model_dump()
        )

        session.add(row)
        session.commit()
        session.refresh(row)

        return {
            "id": row.id,
            "supplier_id":
                row.supplier_id,
            "status": "created"
        }


# -------------------------------------------------
# Demo supplier loader
# -------------------------------------------------
@app.post("/demo/suppliers")
def load_demo_suppliers():

    suppliers = [
        {
            "supplier_id": "SUP101",
            "supplier_name": "Auto Parts One",
            "part_number": "BP-1001",
            "stock": 10,
            "unit_price": Decimal("6500.00"),
            "delivery_days": 1
        },
        {
            "supplier_id": "SUP102",
            "supplier_name": "Mobility Parts",
            "part_number": "BP-1001",
            "stock": 20,
            "unit_price": Decimal("6100.00"),
            "delivery_days": 4
        }
    ]

    inserted = []

    with SessionLocal() as session:

        for supplier in suppliers:

            existing = session.scalar(
                select(SupplierQuote).where(
                    SupplierQuote.supplier_id
                    == supplier["supplier_id"],

                    SupplierQuote.part_number
                    == supplier["part_number"]
                )
            )

            if existing is None:

                session.add(
                    SupplierQuote(**supplier)
                )

                inserted.append(
                    supplier["supplier_id"]
                )

        session.commit()

    return {
        "message": "Demo suppliers loaded",
        "inserted": inserted
    }


# -------------------------------------------------
# Get suppliers for a part
# -------------------------------------------------
@app.get(
    "/parts/{part_number}/suppliers"
)
def get_suppliers(
    part_number: str
):

    with SessionLocal() as session:

        rows = session.scalars(
            select(
                SupplierQuote
            ).where(
                SupplierQuote.part_number
                == part_number,
                SupplierQuote.stock > 0
            )
        ).all()

        return [
            {
                "supplier_id":
                    row.supplier_id,
                "supplier_name":
                    row.supplier_name,
                "part_number":
                    row.part_number,
                "stock":
                    row.stock,
                "unit_price":
                    float(row.unit_price),
                "delivery_days":
                    row.delivery_days
            }
            for row in rows
        ]


# =================================================
# PURCHASE REQUEST APIs
# =================================================

@app.post("/purchase-requests")
def create_purchase_request(
    payload: PurchaseRequestCreate
):

    total_price = (
        payload.unit_price
        * payload.quantity
    )

    with SessionLocal() as session:

        row = PurchaseRequest(
            job_id=payload.job_id,
            supplier_id=
                payload.supplier_id,
            part_number=
                payload.part_number,
            quantity=
                payload.quantity,
            unit_price=
                payload.unit_price,
            total_price=
                total_price,
            status="CREATED"
        )

        session.add(row)
        session.commit()
        session.refresh(row)

        return {
            "pr_id": row.pr_id,
            "job_id": row.job_id,
            "supplier_id":
                row.supplier_id,
            "total_price":
                float(row.total_price),
            "status": row.status
        }


@app.get("/purchase-requests")
def get_purchase_requests():

    with SessionLocal() as session:

        rows = session.scalars(
            select(
                PurchaseRequest
            ).order_by(
                PurchaseRequest.pr_id
            )
        ).all()

        return [
            {
                "pr_id": row.pr_id,
                "job_id": row.job_id,
                "supplier_id":
                    row.supplier_id,
                "part_number":
                    row.part_number,
                "quantity":
                    row.quantity,
                "unit_price":
                    float(row.unit_price),
                "total_price":
                    float(row.total_price),
                "status":
                    row.status
            }
            for row in rows
        ]

@app.get("/purchase-requests")
def get_purchase_requests():

    with SessionLocal() as session:

        requests = session.scalars(
            select(PurchaseRequest)
        ).all()

        return [
            {
                "pr_id": pr.pr_id,
                "job_id": pr.job_id,
                "supplier_id": pr.supplier_id,
                "part_number": pr.part_number,
                "quantity": pr.quantity,
                "unit_price": float(pr.unit_price),
                "total_price": float(pr.total_price),
                "status": pr.status
            }
            for pr in requests
        ]
@app.get("/purchase-requests")
def get_purchase_requests():

    with SessionLocal() as session:

        rows = session.scalars(
            select(
                PurchaseRequest
            ).order_by(
                PurchaseRequest.pr_id
            )
        ).all()

        return [
            {
                "pr_id": row.pr_id,
                "job_id": row.job_id,
                "supplier_id": row.supplier_id,
                "part_number": row.part_number,
                "quantity": row.quantity,
                "unit_price": float(
                    row.unit_price
                ),
                "total_price": float(
                    row.total_price
                ),
                "status": row.status
            }
            for row in rows
        ]