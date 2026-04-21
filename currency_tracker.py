import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

upper_limit = 75.0
lower_limit = 70.0
check_interval = 60
last_status = None


def get_euro():
    api_url = "https://open.er-api.com/v6/latest/EUR"
    response = requests.get(api_url)
    data = response.json()
    afn_rate = data["rates"]["AFN"]
    return afn_rate


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)


print("Programm gestartet...")

while True:
    rate = get_euro()
    print(f"Aktueller Eurokurs: {rate} AFN")

    if rate > upper_limit:
        current_status = "high"
    elif rate < lower_limit:
        current_status = "low"
    else:
        current_status = "normal"

    if current_status != last_status:

        if current_status == "high":
            msg = f"⚠️ Euro ist gestiegen!\nAktueller Preis: {rate} AFN\nObergrenze: {upper_limit}"
            send_telegram(msg)
            print("Telegram-Nachricht wurde gesendet!")

        elif current_status == "low":
            msg = f"⚠️ Euro ist gefallen!\nAktueller Preis: {rate} AFN\nUntergrenze: {lower_limit}"
            send_telegram(msg)
            print("Telegram-Nachricht wurde gesendet!")

        last_status = current_status

    time.sleep(check_interval)