from fastapi import FastAPI
from pydantic import BaseModel, Field

from .database import connection, enabled

app = FastAPI(title="School ERP HR Service", version="1.0.0")


class PayrollRequest(BaseModel):
    employee_id: str
    gross_salary: float = Field(gt=0)
    pension_rate: float = Field(default=0.08, ge=0, le=1)
    tax_rate: float = Field(default=0.1, ge=0, le=1)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "hr"}


@app.post("/payroll")
def calculate_payroll(request: PayrollRequest) -> dict:
    pension = round(request.gross_salary * request.pension_rate, 2)
    tax = round(request.gross_salary * request.tax_rate, 2)
    net = round(request.gross_salary - pension - tax, 2)
    payroll = {"employee_id": request.employee_id, "gross_salary": request.gross_salary, "pension": pension, "tax": tax, "net_salary": net}
    if enabled():
        db_connection = connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute(
                "INSERT INTO hr_payroll (employee_id, gross_salary, pension, tax, net_salary) VALUES (%s, %s, %s, %s, %s)",
                (payroll["employee_id"], payroll["gross_salary"], payroll["pension"], payroll["tax"], payroll["net_salary"]),
            )
            db_connection.commit()
        finally:
            db_connection.close()
    return payroll
