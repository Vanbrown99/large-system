from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="School ERP Academic Service", version="1.0.0")


class Grade(BaseModel):
    course_code: str
    course_name: str
    score: float = Field(ge=0, le=100)
    credit_units: int = Field(ge=1, le=10)


class TranscriptRequest(BaseModel):
    student_id: str
    student_name: str
    grades: list[Grade]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "academic"}


@app.post("/transcripts")
def transcript(request: TranscriptRequest) -> dict:
    total_units = sum(grade.credit_units for grade in request.grades)
    weighted_score = sum(grade.score * grade.credit_units for grade in request.grades)
    average = round(weighted_score / total_units, 2) if total_units else 0
    return {"student_id": request.student_id, "student_name": request.student_name, "average_score": average, "credits": total_units, "standing": "Pass" if average >= 50 else "At Risk", "grades": request.grades}
