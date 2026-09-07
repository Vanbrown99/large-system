from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="School ERP Finance Service", version="1.0.0")


class InvoiceRequest(BaseModel):
    student_id: str
    tuition: float = Field(ge=0)
    accommodation: float = Field(default=0, ge=0)
    other_fees: float = Field(default=0, ge=0)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "finance"}


@app.post("/invoices")
def create_invoice(request: InvoiceRequest) -> dict:
    total = round(request.tuition + request.accommodation + request.other_fees, 2)
    return {"invoice_id": f"INV-{uuid4().hex[:8].upper()}", "student_id": request.student_id, "amount": total, "status": "unpaid"}
