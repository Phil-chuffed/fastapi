from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import requests

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

# Airtable config
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = "Personas"

# Helper to fetch data from Airtable
def fetch_airtable_data():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.text}")

    return response.json().get("records", [])

# Endpoint to list all records
@app.get("/personas")
def get_personas():
    try:
        records = fetch_airtable_data()
        return {"records": records}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Failed to fetch data", "details": str(e)})

# Insight endpoint
@app.get("/insight/female-top-locations")
def female_top_locations():
    try:
        records = fetch_airtable_data()
        location_counts = {}

        for record in records:
            fields = record.get("fields", {})
            if fields.get("gender", "").lower() == "female":
                location = fields.get("location", "Unknown")
                location_counts[location] = location_counts.get(location, 0) + 1

        sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)
        top_3_locations = [{"location": loc, "count": count} for loc, count in sorted_locations[:3]]

        return {"top_3_locations": top_3_locations}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Server error", "details": str(e)})