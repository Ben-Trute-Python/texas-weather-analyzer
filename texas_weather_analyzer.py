import os
import json
from datetime import datetime, timezone
from supabase import create_client, Client

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
    print(f"DEBUG: Supabase list output -> {files}")
    json_files = [f for f in files if f['name'].endswith('.json')]
    
    if not json_files:
        print("⚠️ No raw files found in landing zone.")
        return None
    
    # Sort files by created_at timestamp to get the newest file
    latest_file = max(json_files, key=lambda x: x.get('created_at', x['name']))
    return latest_file['name']

def process_weather_payload(file_name):
    """Downloads raw payload, extracts freeze thresholds, and transforms data."""
    print(f"📥 Downloading {file_name} from Cloud Landing Zone...")
    file_bytes = supabase.storage.from_(BUCKET_NAME).download(file_name)
    raw_data = json.loads(file_bytes.decode('utf-8'))
    
    # Extract hourly metrics from Open-Meteo payload
    hourly = raw_data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    
    transformed_records = []
    freeze_warning_count = 0
    
    for t, temp in zip(times, temps):
        # Freeze condition check (below 32°F / 0°C depending on your units)
        is_freeze = temp <= 0.0  # Open-Meteo defaults to Celsius
        if is_freeze:
            freeze_warning_count += 1
            
        transformed_records.append({
            "timestamp": t,
            "temperature": temp,
            "freeze_warning": is_freeze
        })
        
    print(f"✅ Processed {len(transformed_records)} hourly records.")
    print(f"❄️ Total Freeze Warnings Detected: {freeze_warning_count}")
    
    return transformed_records

if __name__ == "__main__":
    latest_file = get_latest_landing_file()
    if latest_file:
        data = process_weather_payload(latest_file)
