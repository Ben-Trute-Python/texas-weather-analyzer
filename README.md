# ⛅ Texas Weather Analyzer & Automated ETL Data Pipeline

A hybrid Python data architecture featuring an **interactive command-line interface (CLI)** for on-demand historical weather analysis alongside an **automated cloud ETL (Extract, Transform, Load) pipeline** that ingests, cleans, and stores weather metrics directly in a PostgreSQL database with Row Level Security (RLS).

---

## 🛠️ System Architecture

[ Open-Meteo API ]
│
├─► (On-Demand Queries) ──► Interactive CLI Tool (texas_weather_analyzer_v1_legacy.py)
│
└─► (Raw JSON Ingestion) ──► Supabase Storage Landing Zone (raw-weather-landing-zone)
│
▼
Automated Cloud ETL Pipeline (texas_weather_analyzer.py)
│
▼
Supabase PostgreSQL Database (daily_weather_metrics)
---

## 🔑 Key Components

### 1. Automated Backend ETL Pipeline (`texas_weather_analyzer.py`)
* **Extraction:** Ingests raw JSON payloads from the Supabase Cloud Storage landing zone.
* **Transformation:** Cleans time-series data, computes daily minimum temperatures, and maps geographic coordinates dynamically across configured Texas municipalities.
* **Loading:** Idempotently upserts metrics into PostgreSQL (`daily_weather_metrics`) using `(city_name, reading_date)` constraints to prevent duplicate entries.
* **Database Automation:** Leverages database-level calculated columns (`is_light_chill`, `is_freezing`, `is_hard_freeze`) for real-time metric categorization upon insertion.

### 2. Interactive Analysis CLI (`texas_weather_analyzer_v1_legacy.py`)
* **On-Demand Comparisons:** Allows users to pick specific Texas cities and query real-time or historical forecast data.
* **Threshold Flagging:** Detects frost and freeze conditions instantly for agricultural or infrastructure planning.
 This is an end-to-end Python data pipeline that fetches real-time and hi
  Designed specifically for horticultural planning, microclimate e
 
---

 ## 💡 The Problem & Purpose

 Commercial agricultural calculators and standard weather apps ty

 1. **Short-Term Protection:** *Will temperature drop low enough
 2. **Long-Term Feasibility & Labor Planning:** *If I buy land or
 3. **Hardiness Threshold Tracking:** *For zone-marginal crops (e

 This application solves these gaps by providing clear, categorized data.

---

## 🗄️ Database Schema & Governance

The underlying PostgreSQL table (`daily_weather_metrics`) is protected with **Row Level Security (RLS)** and structured as follows:

| Column Name | Data Type | Constraint / Logic |
| :--- | :--- | :--- |
| `id` | `BIGINT` | Primary Key (Auto-incrementing) |
| `city_name` | `VARCHAR` | Unique composite constraint with `reading_date` |
| `latitude` | `FLOAT` | Geographic coordinate |
| `longitude` | `FLOAT` | Geographic coordinate |
| `reading_date` | `DATE` | Unique composite constraint with `city_name` |
| `min_temp_f` | `FLOAT` | Recorded daily low temperature |
| `is_light_chill` | `BOOLEAN` | Calculated column (`min_temp_f <= 45.0`) |
| `is_freezing` | `BOOLEAN` | Calculated column (`min_temp_f <= 32.0`) |
| `is_hard_freeze` | `BOOLEAN` | Calculated column (`min_temp_f <= 28.0`) |
| `created_at` | `TIMESTAMPTZ` | Default `NOW()` timestamp |

---

## 🚀 Getting Started

### Prerequisites
* Python 3.9+
* Supabase Account & PostgreSQL Project
* `pip install supabase python-dotenv`

### Environment Setup
Create a `.env` file in the project root:
```text
SUPABASE_URL=[https://your-supabase-project-id.supabase.co](https://your-supabase-project-id.supabase.co)
SUPABASE_KEY=your-supabase-anon-key
Execution Commands
​Run the backend cloud ETL pipeline:
python texas_weather_analyzer.py
Run the interactive CLI tool:
python texas_weather_analyzer_v1_legacy.py
