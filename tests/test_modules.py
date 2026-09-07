import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).parents[1]
for service in ("academic-service", "finance-service", "hr-service"):
    sys.path.insert(0, str(ROOT / service))

from academic_service.main import app as academic_app
from finance_service.main import app as finance_app
from hr_service.main import app as hr_app


def test_transcript_uses_credit_weighted_average() -> None:
    response = TestClient(academic_app).post(
        "/transcripts",
        json={
            "student_id": "STU-001",
            "student_name": "Demo Student",
            "grades": [
                {"course_code": "A", "course_name": "A", "score": 80, "credit_units": 3},
                {"course_code": "B", "course_name": "B", "score": 50, "credit_units": 1},
            ],
        },
    )
    assert response.status_code == 200
    assert response.json()["average_score"] == 72.5
    assert response.json()["standing"] == "Pass"


def test_invoice_total_is_calculated() -> None:
    response = TestClient(finance_app).post(
        "/invoices",
        json={"student_id": "STU-001", "tuition": 1000, "accommodation": 250, "other_fees": 50},
    )
    assert response.status_code == 200
    assert response.json()["amount"] == 1300
    assert response.json()["status"] == "unpaid"


def test_payroll_deductions_reduce_net_salary() -> None:
    response = TestClient(hr_app).post(
        "/payroll",
        json={"employee_id": "EMP-001", "gross_salary": 5000, "pension_rate": 0.08, "tax_rate": 0.1},
    )
    assert response.status_code == 200
    assert response.json()["pension"] == 400
    assert response.json()["tax"] == 500
    assert response.json()["net_salary"] == 4100
