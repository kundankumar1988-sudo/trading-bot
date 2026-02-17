import requests
import time
import os

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url,data={"chat_id":CHAT_ID,"text":msg})

def strategy(price):
    if price > 25650:
        return "BUY CE 🚀"
    elif price < 25550:
        return "BUY PE 🔻"
    else:
        return "NO TRADE ⏳"

while True:
    try:
        r = requests.get("https://api.indiaapi.in/stock/NIFTY")
        data = r.json()
        price = float(data["ltp"])

        signal = strategy(price)
        send(f"NIFTY: {price} -> {signal}")

        time.sleep(60)

    except Exception as e:
        send("Error: "+str(e))
        time.sleep(60)import requests
import time
import os

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url,data={"chat_id":CHAT_ID,"text":msg})

def strategy(price):
    if price > 25650:
        return "BUY CE 🚀"
    elif price < 25550:
        return "BUY PE 🔻"
    else:
        return "NO TRADE ⏳"

while True:
    try:
        r = requests.get("https://api.indiaapi.in/stock/NIFTY")
        data = r.json()
        price = float(data["ltp"])

        signal = strategy(price)
        send(f"NIFTY: {price} -> {signal}")

        time.sleep(60)

    except Exception as e:
        send("Error: "+str(e))
        time.sleep(60)
