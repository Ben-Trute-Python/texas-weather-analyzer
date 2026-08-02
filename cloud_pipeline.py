import os
import json
import requests
from datetime import datetime, timezone
from supabase import create_client, Client

# 1. Supabase Credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Extract: Fetch raw API payload
API_URL = "https://api.open-meteo.com/v1/forecast?latitude=30.2672&longitude=-97.7431&hourly=temperature_2m"
print("Fetching weather data from API...")
response = requests.get(API_URL)
response.raise_for_status()
raw_data = response.json()

# 3. Create a unique timestamped file path
timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"raw_weather_{timestamp}.json"

# Save locally temporarily
with open(file_name, "w") as f:
    json.dump(raw_data, f)

# 4. Land: Upload the raw JSON payload to Cloud Storage
print(f"Uploading {file_name} to Cloud Landing Zone...")
with open(file_name, "rb") as f:
    supabase.storage.from_("raw-weather-landing-zone").upload(
        path=file_name,
        file=f,
        file_options={"content-type": "application/json"}
    )

print("✅ SUCCESS: Raw API payload successfully landed in the Cloud Landing Zone!")

# Clean up local temporary file
os.remove(file_name)

