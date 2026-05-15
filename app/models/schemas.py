from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ── ESP32 থেকে আসা data ──
class SensorData(BaseModel):
    temperature : float = Field(..., ge=-10,  le=100)
    ph          : float = Field(..., ge=0,    le=14)
    turbidity   : int   = Field(..., ge=0,    le=100)
    status      : str   = Field(..., pattern="^(GOOD|MODERATE|POOR)$")

# ── Dashboard এ যাওয়া data ──
class SensorResponse(BaseModel):
    temperature  : float
    ph           : float
    turbidity    : int
    status       : str
    timestamp    : str

class WeatherData(BaseModel):
    temperature  : float
    humidity     : int
    rainfall     : float
    description  : str

class DashboardResponse(BaseModel):
    sensor       : SensorResponse
    weather      : Optional[WeatherData]
    last_updated : str

# ── History ──
class HistoryPoint(BaseModel):
    time         : str
    temperature  : float
    ph           : float
    turbidity    : int
    status       : str