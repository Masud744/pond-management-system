from fastapi import APIRouter, HTTPException
from app.models.schemas import SensorData
from app.services.influx_service import save_sensor_data
from app.services.alert_service import check_and_alert
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/sensor")
async def receive_sensor_data(data: SensorData):
    """ESP32 থেকে sensor data receive করে"""

    # InfluxDB তে save
    saved = save_sensor_data(
        temp      = data.temperature,
        ph        = data.ph,
        turbidity = data.turbidity,
        status    = data.status
    )

    if not saved:
        raise HTTPException(status_code=500, detail="Database save failed")

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