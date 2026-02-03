import time
import requests
from telegram import Bot

TOKEN = "ВСТАВЬ_СЮДА_TOKEN"
CHAT_ID = -1001234567890   # твой chat_id
CHECK_INTERVAL = 60

API_URL = "https://alerts.in.ua/api/states"

bot = Bot(token=TOKEN)
last_state = False

def check_alert():
    global last_state
    try:
        data = requests.get(API_URL, timeout=10).json()
        alert_now = False

        for region in data:
            if region["name"] == "Одеська область":
                for district in region["districts"]:
                    if district["name"] == "Одеський район":
                        alert_now = district["alert"]

        if alert_now and not last_state:
            bot.send_message(chat_id=CHAT_ID, text="ВОЗДУШНАЯ ТРЕВОГА")
            last_state = True

        elif not alert_now and last_state:
            bot.send_message(chat_id=CHAT_ID, text="ОТБОЙ ТРЕВОГИ")
            last_state = False

    except Exception as e:
        print("Ошибка:", e)

while True:
    check_alert()
    time.sleep(CHECK_INTERVAL)
