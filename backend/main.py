from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import engine, Base, SessionLocal
import models


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Sustainable Tours Travel API",
    description="Backend API for the Sustainable Tours Travel Project",
    version="1.0.0"
)


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Trip Data Structure
# -------------------------

class Trip(BaseModel):
    name: str
    destination: str


# -------------------------
# HOME API
# -------------------------

@app.get("/")
def home():
    return {
        "message": "Sustainable Tours Travel API is running"
    }


# -------------------------
# CREATE / ADD TRIP
# -------------------------

@app.post("/trips")
def add_trip(trip: Trip):

    db = SessionLocal()

    new_trip = models.Trip(
        name=trip.name,
        destination=trip.destination
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    result = {
        "message": "Trip saved successfully",
        "trip": {
            "id": new_trip.id,
            "name": new_trip.name,
            "destination": new_trip.destination
        }
    }

    db.close()

    return result


# -------------------------
# READ / GET ALL TRIPS
# -------------------------

@app.get("/trips")
def get_trips():

    db = SessionLocal()

    trips = db.query(models.Trip).all()

    result = []

    for trip in trips:
        result.append({
            "id": trip.id,
            "name": trip.name,
            "destination": trip.destination
        })

    db.close()

    return result


# -------------------------
# UPDATE / EDIT TRIP
# -------------------------

@app.put("/trips/{trip_id}")
def update_trip(trip_id: int, trip: Trip):

    db = SessionLocal()

    existing_trip = db.query(models.Trip).filter(
        models.Trip.id == trip_id
    ).first()

    if existing_trip is None:
        db.close()

        return {
            "message": "Trip not found"
        }

    existing_trip.name = trip.name
    existing_trip.destination = trip.destination

    db.commit()
    db.refresh(existing_trip)

    result = {
        "message": "Trip updated successfully",
        "trip": {
            "id": existing_trip.id,
            "name": existing_trip.name,
            "destination": existing_trip.destination
        }
    }

    db.close()

    return result


# -------------------------
# DELETE TRIP
# -------------------------

@app.delete("/trips/{trip_id}")
def delete_trip(trip_id: int):

    db = SessionLocal()

    trip = db.query(models.Trip).filter(
        models.Trip.id == trip_id
    ).first()

    if trip is None:
        db.close()

        return {
            "message": "Trip not found"
        }

    db.delete(trip)
    db.commit()
    db.close()

    return {
        "message": "Trip deleted successfully"
    }