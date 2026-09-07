FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY finance-service/finance_service ./finance_service
EXPOSE 8003
CMD ["uvicorn", "finance_service.main:app", "--host", "0.0.0.0", "--port", "8003"]
