FROM python:3.12-alpine
WORKDIR /PaymentService
COPY requirements.txt .
RUN apk add --no-cache postgresql-dev gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["uvicorn", "payment_service:app", "--host","0.0.0.0","--port","5001"]
