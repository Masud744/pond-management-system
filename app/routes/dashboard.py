from fastapi import APIRouter, Query
from app.services.influx_service import get_latest_reading, get_history
from app.services.weather_service import get_weather
from datetime import datetime, timezone

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_data():
    """Dashboard এর জন্য latest data + weather"""

    sensor  = get_latest_reading()
    weather = get_weather()

    return {
        "sensor"       : sensor,
        "weather"      : weather,
        "last_updated" : datetime.now(timezone.utc).isoformat()
    }


@router.get("/history")
async def get_sensor_history(hours: int = Query(default=24, ge=1, le=168)):
    """Last N ঘন্টার history data — default 24 ঘন্টা"""

    history = get_history(hours=hours)

    return {
        "hours"   : hours,
        "count"   : len(history),
        "data"    : history
    }


@router.get("/status")
async def get_current_status():
    """শুধু current water status"""

    sensor = get_latest_reading()

    if not sensor:
        return {"status": "UNKNOWN", "message": "No data yet"}

    return {
        "status"      : sensor["status"],
        "temperature" : sensor["temperature"],
        "ph"          : sensor["ph"],
        "turbidity"   : sensor["turbidity"],
        "timestamp"   : sensor["timestamp"]
    }