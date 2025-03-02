from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("PAYMENT_DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("PAYMENT_DATABASE_URL is not set in .env")

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Payment Model (Stores transactions)
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    account_id = Column(Integer, nullable=False)
    booking_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(20), default="SUCCESS")
    created_at = Column(DateTime, default=datetime.utcnow)

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI()

# Dependency: Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define Pydantic Model for Payment Request
class PaymentRequest(BaseModel):
    id: int
    account_id: int
    booking_id: int
    amount: int

# Correct API: Process Payment (Accepts JSON via Pydantic Model)
@app.post("/payments")
def process_payment(payment_data: PaymentRequest, db: Session = Depends(get_db)):
    if payment_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid payment amount")

    # Store transaction
    new_payment = Payment(
        user_id=payment_data.id,
        account_id=payment_data.account_id,
        booking_id=payment_data.booking_id,
        amount=payment_data.amount,
        status="SUCCESS"
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return {"message": "Payment successful", "transaction_id": new_payment.id}