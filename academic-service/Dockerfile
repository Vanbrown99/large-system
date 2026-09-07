FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY academic-service/academic_service ./academic_service
EXPOSE 8002
CMD ["uvicorn", "academic_service.main:app", "--host", "0.0.0.0", "--port", "8002"]
