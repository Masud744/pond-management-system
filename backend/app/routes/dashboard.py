from fastapi import APIRouter, Query
from app.services.weather_service import get_weather
from app.routes.sensor import latest_sensor_data, sensor_history_data
from datetime import datetime, timezone

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_data():
    """Dashboard এর জন্য latest data + weather"""
    return {
        "sensor"       : latest_sensor_data,
        "weather"      : get_weather(),
        "last_updated" : datetime.now(timezone.utc).isoformat()
    }


@router.get("/history")
async def get_sensor_history(hours: int = Query(default=24, ge=1, le=168)):
    """Last N ঘন্টার history data"""
    return {
        "hours"   : hours,
        "count"   : len(sensor_history_data),
        "data"    : sensor_history_data
    }


@router.get("/status")
async def get_current_status():
    """শুধু current water status"""
    if not latest_sensor_data:
        return {"status": "UNKNOWN", "message": "No data yet"}

    return {
        "status"      : latest_sensor_data["status"],
        "temperature" : latest_sensor_data["temperature"],
        "ph"          : latest_sensor_data["ph"],
        "turbidity"   : latest_sensor_data["turbidity"],
        "timestamp"   : latest_sensor_data["timestamp"]
    }