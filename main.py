from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import requests
from collections import Counter

app = FastAPI()

# Confirm app is live
@app.get("/")
def read_root():
    return {
        "greeting": "Hello, Phil!",
        "message": "You're running your own FastAPI app now 🚀"
    }

# Dummy POST endpoint
class PersonaRequest(BaseModel):
    age: int
    location: str
    income: str

@app.post("/generate")
def generate_persona(data: PersonaRequest):
    return {
        "summary": f"A {data.age}-year-old from {data.location} earning {data.income}."
    }

# Airtable connection
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = "Personas"

@app.get("/personas")
def get_personas():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch data", "details": response.text}

    return response.json()

@app.get("/insight/female-top-locations")
async def female_top_locations():
    records = await fetch_airtable_data()
    location_counts = {}

    for record in records:
        fields = record.get("fields", {})
        if fields.get("gender", "").lower() == "female":
            location = fields.get("location", "Unknown")
            location_counts[location] = location_counts.get(location, 0) + 1

    sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)
    top_3_locations = [{"location": loc, "count": count} for loc, count in sorted_locations[:3]]

    return {"top_3_locations": top_3_locations}