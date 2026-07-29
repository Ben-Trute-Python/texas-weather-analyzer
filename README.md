# Texas Weather & Freeze Threshold Analyzer 🌡️❄️

An end-to-end Python data pipeline that fetches real-time and historical weather data for 45+ agricultural regions, state parks, and coastal areas across Texas using the Open-Meteo REST API and persists structured readings into a SQLite database.

Designed specifically for horticultural planning, microclimate evaluation, and risk mitigation, this tool automates localized freeze/frost tracking to guide crop protection and agricultural site selection.

---

## 💡 The Problem & Purpose

Commercial agricultural calculators and standard weather apps typically focus on simple 7-day forecasts or broad USDA Hardiness Zones based on multi-decade averages. They often fail to answer critical, practical questions for growers working in marginal zones or high-risk microclimates:

1. **Short-Term Protection:** *Will temperature drop low enough tonight or this week that I need to cover frost-sensitive crops?*
2. **Long-Term Feasibility & Labor Planning:** *If I buy land or relocate to a specific town, how many days per winter will I realistically spend covering plants or running freeze-protection equipment?*
3. **Hardiness Threshold Tracking:** *For zone-marginal crops (e.g., Zone 9 perennials hardy to 20°F), how frequently do freezes below 20°F actually occur over the past 5 winters?*

This application solves these gaps by providing clear, categorized temperature-band metrics for both immediate decision-making and 5-year historical risk assessments across evaluated Texas regions.

---

## 🏗️ Architecture & Features

* **API Ingestion (Extract):** Leverages Python `requests` with defensive error handling (timeouts, status validation, fallback defaults) to pull meteorological data.
* **SQL Persistence (Load):** Automated SQLite database module (`database.py`) that initializes schemas, prevents SQL injection using parameterized queries (`?`), and tracks automated timestamps for historical audit trails.
* **Modular Software Architecture:** Centralized location configuration (`config.py`) shared seamlessly across analysis tools and app interfaces.
* **Threshold Analysis (Transform):** Processes daily minimum temperatures into frost  and freeze band analytics (`<=32°F`, `<20°F`, `33-35°F`).

* **Dynamic API Routing:** Seamlessly switches between Open-Meteo's **Forecast API** (for upcoming 7-day outlooks) and the **Historical Weather Archive API** (for multi-year winter analysis).
* **Categorized Temperature Bands:**
  * **Light Chill / Frost Warning (33°F  - 35°F ):** Identifies near-freezing conditions requiring row covers or frost cloth.
  * **Freezing Threshold (<= 32°F ):** Tracks total freeze days affecting sensitive tissues.
  * **Hard Freeze / Zone 9 Limit (< 20°F ):** Evaluates extreme cold events critical for determining the survival frequency of Zone 9 perennials.
* **5-Winter Historical Audit:** Evaluates historical winter data blocks (Nov 1 – Mar 31) across the last 5 full seasons to provide an accurate representation of near-future climate trends.
* **Interactive CLI Interface:** Clean, user-friendly terminal menu for quick city selection and analysis mode switching.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3
* **Libraries:** `requests`
* **Data Provider:** [Open-Meteo API](https://open-meteo.com/) (Forecast & Archive Endpoints)

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3 installed along with the `requests` library:

```bash
pip install requests
```

## 🚀 How to Run
1. Clone the repository:

```bash
git clone https://github.com/Ben-Trute-Python/texas-weather-analyzer.git
```

2. Run the pipeline: 
```bash
python texas_weather_analyzer.py
```

3. Inspect stored database records:
```bash
python -c "import database; print(database.get_all_readings()[:5])"
```
