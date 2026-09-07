import json
import os

import pika
from fastapi import FastAPI
from fastapi import HTTPException, status
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


class EnrollmentRequest(BaseModel):
    student_id: str = Field(min_length=1, max_length=50)
    tuition: float = Field(ge=0)
    accommodation: float = Field(default=0, ge=0)
    other_fees: float = Field(default=0, ge=0)


def publish_enrollment(request: EnrollmentRequest) -> None:
    host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, connection_attempts=3, retry_delay=1))
    try:
        channel = connection.channel()
        channel.queue_declare(queue="student.enrolled", durable=True)
        channel.basic_publish(
            exchange="",
            routing_key="student.enrolled",
            body=json.dumps(request.model_dump()).encode(),
            properties=pika.BasicProperties(delivery_mode=2, content_type="application/json"),
        )
    finally:
        connection.close()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "academic"}


@app.post("/transcripts")
def transcript(request: TranscriptRequest) -> dict:
    total_units = sum(grade.credit_units for grade in request.grades)
    weighted_score = sum(grade.score * grade.credit_units for grade in request.grades)
    average = round(weighted_score / total_units, 2) if total_units else 0
    return {"student_id": request.student_id, "student_name": request.student_name, "average_score": average, "credits": total_units, "standing": "Pass" if average >= 50 else "At Risk", "grades": request.grades}


@app.post("/enrollments", status_code=status.HTTP_202_ACCEPTED)
def enroll(request: EnrollmentRequest) -> dict[str, str]:
    try:
        publish_enrollment(request)
    except (pika.exceptions.AMQPError, OSError) as error:
        raise HTTPException(status_code=503, detail="Message broker unavailable") from error
    return {"status": "accepted", "event": "StudentEnrolled", "student_id": request.student_id}
