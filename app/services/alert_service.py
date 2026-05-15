import requests
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# শেষ কোন status এ alert পাঠানো হয়েছে track করি
# যাতে বারবার একই alert না যায়
last_alerted_status = "GOOD"


def send_telegram(message: str):
    """Telegram এ message পাঠায়"""
    try:
        url  = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id"    : settings.TELEGRAM_CHAT_ID,
            "text"       : message,
            "parse_mode" : "HTML"
        }
        response = requests.post(url, data=data, timeout=5)
        if response.status_code == 200:
            logger.info("Telegram alert sent ✓")
            return True
        else:
            logger.warning(f"Telegram failed: {response.text}")
            return False

    except Exception as e:
        logger.error(f"Telegram error: {e}")
        return False


def check_and_alert(status: str, temp: float, ph: float, turbidity: int):
    """Status খারাপ হলে Telegram alert পাঠায়"""
    global last_alerted_status

    # একই status এ আগে alert গেলে আবার পাঠাবো না
    if status == last_alerted_status:
        return

    if status == "POOR":
        message = (
            "🚨 <b>POND ALERT — WATER POOR!</b>\n\n"
            f"🌡️ Temperature : {temp:.1f}°C\n"
            f"🧪 pH          : {ph:.2f}\n"
            f"🌊 Turbidity   : {turbidity}%\n\n"
            "⚠️ Fish feeding stopped automatically!\n"
            "🧹 Manual cleaning required!"
        )
        send_telegram(message)

    elif status == "MODERATE":
        message = (
            "⚠️ <b>POND WARNING — WATER MODERATE</b>\n\n"
            f"🌡️ Temperature : {temp:.1f}°C\n"
            f"🧪 pH          : {ph:.2f}\n"
            f"🌊 Turbidity   : {turbidity}%\n\n"
            "👁️ Please monitor the pond closely."
        )
        send_telegram(message)

    elif status == "GOOD" and last_alerted_status in ["POOR", "MODERATE"]:
        # পানি আবার ভালো হলে recovery alert
        message = (
            "✅ <b>POND RECOVERED — WATER GOOD</b>\n\n"
            f"🌡️ Temperature : {temp:.1f}°C\n"
            f"🧪 pH          : {ph:.2f}\n"
            f"🌊 Turbidity   : {turbidity}%\n\n"
            "🐟 Fish feeding resumed!"
        )
        send_telegram(message)

    last_alerted_status = status