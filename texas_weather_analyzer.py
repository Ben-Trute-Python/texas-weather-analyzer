import os
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
from supabase import create_client, Client
from config import TEXAS_CITIES

# Load environment variables from .env
load_dotenv()

# 1. Initialize Supabase Connection
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET_NAME = "raw-weather-landing-zone"


def get_latest_landing_file():
    """Finds the most recent raw JSON payload in the landing zone bucket."""
    files = supabase.storage.from_(BUCKET_NAME).list()
    json_files = [f for f in files if f['name'].endswith('.json')]

    if not json_files:
        print("⚠️ No raw files found in landing zone.")
        return None

    # Sort files by created_at timestamp to get the newest file
    latest_file = max(json_files, key=lambda x: x.get('created_at', x['name']))
    return latest_file['name']


def save_daily_metric_to_postgres(city_name: str, lat: float, lon: float, reading_date: str, min_temp_f: float):
    """Sends processed daily minimum temperature to Supabase Postgres idempotently."""
    payload = {
        "city_name": city_name,
        "latitude": lat,
        "longitude": lon,
        "reading_date": reading_date,
        "min_temp_f": min_temp_f
    }
    try:
        response = supabase.table("daily_weather_metrics").upsert(
            payload, 
            on_conflict="city_name,reading_date"
        ).execute()
        print(f" Saved {city_name} metric ({min_temp_f}°F on {reading_date}) to Postgres.")
        return response.data
    except Exception as e:
        print(f"⚠️ Failed to write metric to Postgres for {city_name}: {e}")
        return None


def process_weather_payload(file_name):
    """Downloads raw payload, transforms data, and loads metrics for configured cities into Postgres."""
    print(f"📥 Downloading {file_name} from Cloud Landing Zone...")
    file_bytes = supabase.storage.from_(BUCKET_NAME).download(file_name)
    raw_data = json.loads(file_bytes.decode('utf-8'))

    # Extract hourly metrics from Open-Meteo payload
    hourly = raw_data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])

    if not temps or not times:
        print("⚠️ Weather payload does not contain complete hourly time/temperature arrays.")
        return

    # Extract daily low and reading date
    min_temp = min(temps)
    reading_date = times[0].split("T")[0]

    # Check if payload specifies a city; otherwise process all cities in TEXAS_CITIES config
    payload_city = raw_data.get("city")

    if payload_city and payload_city in TEXAS_CITIES:
        # Process single specified city from payload
        lat = TEXAS_CITIES[payload_city]["lat"]
        lon = TEXAS_CITIES[payload_city]["lon"]
        save_daily_metric_to_postgres(payload_city, lat, lon, reading_date, min_temp)
    else:
        # Process all configured Texas cities dynamically
        print(f"⚡ Processing metrics across {len(TEXAS_CITIES)} configured Texas cities...")
        for city_name, coords in TEXAS_CITIES.items():
            save_daily_metric_to_postgres(
                city_name=city_name,
                lat=coords["lat"],
                lon=coords["lon"],
                reading_date=reading_date,
                min_temp_f=min_temp
            )

    print(" Cloud ETL Pipeline Execution Complete!")


if __name__ == "__main__":
    latest_file = get_latest_landing_file()
    if latest_file:
        process_weather_payload(latest_file)
