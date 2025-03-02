from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import requests
import jsonwebtoken as jwt
import pika
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL")
EVENT_SERVICE_URL = os.getenv("EVENT_SERVICE_URL")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")
JWT_SECRET = os.getenv("JWT_SECRET")

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Booking Model
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)
    tickets = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False)
    status = Column(Enum("PENDING", "CONFIRMED", name="booking_status"), default="PENDING")

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Dependency: Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency: Verify JWT token
def verify_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]  # Bearer <token>
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Pydantic models
class BookingCreate(BaseModel):
    event_id: int
    tickets: int

class BookingConfirm(BaseModel):
    booking_id: int 
    amount: int
    account_id: int

# API: Create a Booking (PENDING status)
@app.post("/bookings")
def create_booking(
    booking_data: BookingCreate, 
    user_data: dict = Depends(verify_token), 
    db: Session = Depends(get_db)
):
    # Check event availability
    event_response = requests.get(f"{EVENT_SERVICE_URL}/events/{booking_data.event_id}/availability")
    if event_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Event not found")

    event_data = event_response.json()
    if event_data["available_tickets"] < booking_data.tickets:
        raise HTTPException(status_code=400, detail="Not enough tickets available")

    # Calculate total amount
    total_amount = booking_data.tickets * event_data["ticket_price"]

    # Save booking in DB
    new_booking = Booking(
        user_id=user_data["id"],
        event_id=booking_data.event_id,
        tickets=booking_data.tickets,
        total_amount=total_amount
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return {"booking_id": new_booking.id, "total_amount": total_amount, "status": "PENDING"}

# API: Confirm Booking (Calls Payment Service)
@app.post("/bookings/confirm")
def confirm_booking(
    confirmation_data: BookingConfirm, 
    user_data: dict = Depends(verify_token), 
    db: Session = Depends(get_db)
):
    # Retrieve booking
    booking = db.query(Booking).filter(Booking.id == confirmation_data.booking_id, Booking.user_id == user_data["id"]).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found or unauthorized")

    if booking.status == "CONFIRMED":
        raise HTTPException(status_code=400, detail="Booking already confirmed")

    if booking.total_amount != confirmation_data.amount:
        raise HTTPException(status_code=400, detail="Incorrect payment amount")

    # Call Payment Service
    payment_response = requests.post(
        f"{PAYMENT_SERVICE_URL}/payments",
        json={
            "id": user_data["id"],
            "account_id": confirmation_data.account_id,
            "booking_id": confirmation_data.booking_id,
            "amount": confirmation_data.amount
        }
    )

    if payment_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Payment failed")

    # Update booking status to CONFIRMED
    booking.status = "CONFIRMED"
    db.commit()

    # Publish event to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    message = {
        "booking_id": confirmation_data.booking_id,
        "user_id": user_data["id"],
        "status": "CONFIRMED"
    }

    channel.basic_publish(
        exchange="",
        routing_key=RABBITMQ_QUEUE,
        body=str(message)
    )
    connection.close()

    return {"message": "Booking confirmed successfully"}