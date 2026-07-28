import sqlite3

# 1. Connect to SQLite database (creates 'weather_data.db' automatically if missing)
conn = sqlite3.connect("weather_data.db")
cursor = conn.cursor()

# 2. Create the table
cursor.execute("DROP TABLE IF EXISTS freeze_logs")
cursor.execute("""
CREATE TABLE IF NOT EXISTS freeze_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    date TEXT,
    min_temp REAL,
    category TEXT
)
""")

# 3. Dummy data to simulate API payload parsing
sample_data = [
    ("Victoria", "2026-01-10", 34.0, "Light Chill"),
    ("Victoria", "2026-01-11", 31.0, "Freeze"),
    ("Victoria", "2026-01-12", 18.5, "Hard Freeze"),
    ("Lubbock", "2026-01-10", 22.0, "Freeze"),
    ("Lubbock", "2026-01-11", 14.0, "Hard Freeze")
]

# 4. Insert multiple records efficiently using executemany
cursor.executemany("""
INSERT INTO freeze_logs (city, date, min_temp, category)
VALUES (?, ?, ?, ?)
""", sample_data)

# Save (commit) the inserts to disk
conn.commit()

print("✅ Data successfully loaded into SQLite database!\n")

# 5. Execute SQL Query: Get count of freeze events grouped by category for Victoria
print("--- Victoria Freeze Event Summary ---")
query = """
SELECT category, COUNT(*) 
FROM freeze_logs 
WHERE city = 'Victoria' 
GROUP BY category
"""

cursor.execute(query)
results = cursor.fetchall()

for category, count in results:
    print(f"{category}: {count} day(s)")

# Always close the connection when done
conn.close()
