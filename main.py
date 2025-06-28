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
def female_top_locations():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return JSONResponse(status_code=500, content={"error": "Failed to fetch data", "details": response.text})

    records = response.json().get("records", [])

    # Extract locations of females
    female_locations = [
        record["fields"].get("Location")
        for record in records
        if record["fields"].get("Gender") == "Female" and record["fields"].get("Location")
    ]

    # Count and return top 3
    top_3 = Counter(female_locations).most_common(3)

    return {
        "insight": "Top 3 locations for females",
        "results": [location for location, count in top_3]
    }