import requests
from config import TEXAS_CITIES

def fetch_daily_lows(lat, lon, mode="forecast", start_date=None, end_date=None):
    """Fetches 7-day daily minimum temperatures in Fahrenheit."""
    if mode == "history":
        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_min&temperature_unit=fahrenheit&timezone=auto"
    else:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_min&temperature_unit=fahrenheit&timezone=auto"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json().get("daily", {}).get("temperature_2m_min", [])
        return []
    except requests.exceptions.RequestException as e:
        print(f"Network call failed: {e}")
        return []

def analyze_chill_bands(temps):
    """Categorizes temperatures into specific chill thresholds (Fahrenheit)."""
    light_chill = sum(1 for t in temps if 33 <= t < 36) # < 36 but above freezing
    freezing = sum(1 for t in temps if t <= 32)         # <= 32
    hard_freeze = sum(1 for t in temps if t < 20)      # < 20
    
    return {
        "light_chill": light_chill,
        "freezing": freezing,
        "hard_freeze": hard_freeze
    }

def main():
    print("=== Texas Winter Threshold Analyzer ===")
    print("Available Cities:", ", ".join(TEXAS_CITIES.keys()))
    
    city = input("Select a city: ").strip().title()
    if city not in TEXAS_CITIES:
        print("City not recognized.")
        return

    coords = TEXAS_CITIES[city]

    print("\nSelect Analysis Mode:", flush=True)
    print("1. Upcoming 7-Day Forecast")
    print("2. Historical Winter Analysis (Past 5 Winters)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "2":
        # Historical Loop (Last 5 Winters)
        winters = [
            {"label": "2025-2026", "start": "2025-11-01", "end": "2026-03-31"},
            {"label": "2024-2025", "start": "2024-11-01", "end": "2025-03-31"},
            {"label": "2023-2024", "start": "2023-11-01", "end": "2024-03-31"},
            {"label": "2022-2023", "start": "2022-11-01", "end": "2023-03-31"},
            {"label": "2021-2022", "start": "2021-11-01", "end": "2022-03-31"},
        ]
        
        print(f"\n--- Historical 5-Winter Analysis for {city} (°F) ---")
        for w in winters:
            temps = fetch_daily_lows(coords["lat"], coords["lon"], mode="history", start_date=w["start"], end_date=w["end"])
            if temps:
                results = analyze_chill_bands(temps)
                print(f"Winter {w['label']}: {results['light_chill']} light chill (33-35°F) | {results['freezing']} freezing (<=32°F) | {results['hard_freeze']} hard freeze (<20°F)")
            else:
                print(f"Winter {w['label']}: Failed to retrieve data")
    else:
        # Standard Forecast Mode
        temps = fetch_daily_lows(coords["lat"], coords["lon"], mode="forecast")
        if not temps:
            print("Could not retrieve forecast data.")
            return

        results = analyze_chill_bands(temps)
        print(f"\n--- 7-Day Low Temperature Forecast for {city} (°F) ---")
        print(f"Days between 33°F and 35°F: {results['light_chill']}")
        print(f"Days 32°F or below:       {results['freezing']}")
        print(f"Days below 20")

if __name__ == "__main__":
    main()
