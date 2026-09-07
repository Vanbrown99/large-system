FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY hr-service/hr_service ./hr_service
EXPOSE 8004
CMD ["uvicorn", "hr_service.main:app", "--host", "0.0.0.0", "--port", "8004"]
