import sqlite3

DB_NAME = "weather_data.db"

def init_db():
    """Initializes the SQLite database and creates the weather table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            temperature REAL,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def save_weather_reading(location_name: str, lat: float, lon: float, temp: float):
    """Inserts a single weather reading cleanly into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO weather_records (location_name, latitude, longitude, temperature)
        VALUES (?, ?, ?, ?)
    """, (location_name, lat, lon, temp))
    
    conn.commit()
    conn.close()

def get_all_readings():
    """Fetches all stored weather readings from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, location_name, latitude, longitude, temperature, fetched_at FROM weather_records ORDER BY fetched_at DESC")
    rows = cursor.fetchall()
    
    conn.close()
    return rows
