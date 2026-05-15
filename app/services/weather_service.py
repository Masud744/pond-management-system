import requests
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def get_weather():
    """OpenWeatherMap থেকে current weather আনে"""
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={settings.OPENWEATHER_CITY},{settings.OPENWEATHER_COUNTRY}"
            f"&appid={settings.OPENWEATHER_API_KEY}"
            f"&units=metric"
        )
        response = requests.get(url, timeout=5)
        data     = response.json()

        if response.status_code != 200:
            logger.warning(f"Weather API error: {data}")
            return None

        # Rainfall থাকে শুধু বৃষ্টি হলে
        rainfall = 0.0
        if "rain" in data:
            rainfall = data["rain"].get("1h", 0.0)

        return {
            "temperature" : data["main"]["temp"],
            "humidity"    : data["main"]["humidity"],
            "rainfall"    : rainfall,
            "description" : data["weather"][0]["description"]
        }

    except Exception as e:
        logger.error(f"Weather fetch error: {e}")
        return None