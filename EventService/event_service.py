from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import jsonwebtoken as jwt
import os
import datetime
from functools import wraps

# Load environment variables from .env
load_dotenv()

# Flask App
app = Flask(__name__)

# Secret Key for JWT
JWT_SECRET = os.getenv("JWT_SECRET")

# MongoDB Setup
MONGO_URI = os.getenv("MONGO_URI")  # Load from .env
client = MongoClient(MONGO_URI)

# Change the database name to "EventBooking" (as per .env)
db = client["EventBooking"]

# Collections
events_collection = db["events"]
counters_collection = db["counters"]

# Function to get the next auto-incrementing event_id
def get_next_event_id():
    counter = counters_collection.find_one_and_update(
        {"_id": "event_id"},
        {"$inc": {"seq": 1}},  # Increment the counter by 1
        return_document=True
    )
    return counter["seq"]

# Middleware: Verify JWT Token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        
        try:
            token = token.split(" ")[1]  # Extract token from "Bearer <token>"
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user = decoded_token  # Attach user details to request
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        
        return f(*args, **kwargs)
    
    return decorated

# Middleware: Restrict Access to Event Managers
def event_manager_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, "user") or request.user.get("usertype") != "eventmanager":
            return jsonify({"error": "Access denied. Only event managers can create events."}), 403
        return f(*args, **kwargs)
    
    return decorated

# Get all events
@app.route('/events', methods=['GET'])
@token_required
def get_events():
    events = list(events_collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectId
    return jsonify(events), 200

# Add a new event (Only Event Managers)
@app.route('/events', methods=['POST'])
@token_required
@event_manager_required
def create_event():
    if not request.is_json:  # Check if request contains JSON
        return jsonify({"error": "Request must be JSON"}), 415
    data = request.json
    required_fields = ["name", "date", "location", "capacity", "booked_tickets", "ticket_price"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    new_event_id = get_next_event_id()  # Get next available ID

    event_data = {
        "event_id": new_event_id,
        "name": data["name"],
        "date": data["date"],
        "location": data["location"],
        "capacity": data["capacity"],
        "booked_tickets": data["booked_tickets"],
        "ticket_price": data["ticket_price"]
    }

    events_collection.insert_one(event_data)
    return jsonify({"message": "Event created successfully", "event_id": new_event_id}), 201

# Get event by ID
@app.route('/events/<int:event_id>', methods=['GET'])
@token_required
def get_event(event_id):
    event = events_collection.find_one({"event_id": event_id}, {"_id": 0})
    if event:
        return jsonify(event), 200
    return jsonify({"error": "Event not found"}), 404

# Check event availability (For Booking Service)
@app.route('/events/<int:event_id>/availability', methods=['GET'])
def check_event_availability(event_id):
    event = events_collection.find_one({"event_id": event_id}, {"_id": 0})
    if not event:
        return jsonify({"error": "Event not found"}), 404

    available_tickets = event["capacity"] - event["booked_tickets"]
    return jsonify({
        "event_id": event_id,
        "available_tickets": available_tickets,
        "ticket_price": event["ticket_price"]
    }), 200

if __name__ == '__main__':
    app.run(debug=True)