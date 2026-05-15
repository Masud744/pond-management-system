from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # ── InfluxDB ──
    INFLUXDB_URL    = os.getenv("INFLUXDB_URL")
    INFLUXDB_TOKEN  = os.getenv("INFLUXDB_TOKEN")
    INFLUXDB_ORG    = os.getenv("INFLUXDB_ORG")
    INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")

    # ── OpenWeather ──
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    OPENWEATHER_CITY    = os.getenv("OPENWEATHER_CITY", "Dhaka")
    OPENWEATHER_COUNTRY = os.getenv("OPENWEATHER_COUNTRY", "BD")

    # ── Telegram ──
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")

    # ── Water Quality Thresholds ──
    PH_GOOD_MIN   = 6.5
    PH_GOOD_MAX   = 8.5
    PH_MOD_MIN    = 6.0
    PH_MOD_MAX    = 9.0
    TEMP_GOOD_MIN = 20.0
    TEMP_GOOD_MAX = 32.0
    TURB_GOOD_MAX = 30
    TURB_MOD_MAX  = 60

settings = Settings()