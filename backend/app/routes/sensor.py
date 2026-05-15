from fastapi import APIRouter, HTTPException
from app.models.schemas import SensorData
from app.services.alert_service import check_and_alert
from datetime import datetime, timezone
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Temporary IN-MEMORY storage to bypass InfluxDB
latest_sensor_data = None
sensor_history_data = []

@router.post("/sensor")
async def receive_sensor_data(data: SensorData):
    """ESP32 থেকে sensor data receive করে"""
    global latest_sensor_data, sensor_history_data

    # Save to memory instead of InfluxDB
    latest_sensor_data = {
        "temperature": data.temperature,
        "ph": data.ph,
        "turbidity": data.turbidity,
        "status": data.status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Keep last 50 records in history
    sensor_history_data.append(latest_sensor_data)
    if len(sensor_history_data) > 50:
        sensor_history_data.pop(0)

    # Alert check
    check_and_alert(
        status    = data.status,
        temp      = data.temperature,
        ph        = data.ph,
        turbidity = data.turbidity
    )

    logger.info(f"Data received → {data.status}")

    return {
        "success" : True,
        "message" : "Data saved",
        "status"  : data.status
    }