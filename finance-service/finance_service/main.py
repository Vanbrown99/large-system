import json
import os
import threading
from uuid import uuid4

import pika
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="School ERP Finance Service", version="1.0.0")
invoices: list[dict] = []


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
    invoice = {"invoice_id": f"INV-{uuid4().hex[:8].upper()}", "student_id": request.student_id, "amount": total, "status": "unpaid"}
    invoices.append(invoice)
    return invoice


def consume_enrollments() -> None:
    host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, connection_attempts=3, retry_delay=2))
            channel = connection.channel()
            channel.queue_declare(queue="student.enrolled", durable=True)

            def handle_event(channel, method, properties, body) -> None:
                event = json.loads(body)
                create_invoice(InvoiceRequest(**event))
                channel.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue="student.enrolled", on_message_callback=handle_event)
            channel.start_consuming()
        except (pika.exceptions.AMQPError, OSError, json.JSONDecodeError, ValueError):
            continue


@app.on_event("startup")
def start_consumer() -> None:
    threading.Thread(target=consume_enrollments, daemon=True, name="enrollment-consumer").start()


@app.get("/invoices/{student_id}")
def list_invoices(student_id: str) -> list[dict]:
    return [invoice for invoice in invoices if invoice["student_id"] == student_id]
