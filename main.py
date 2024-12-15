import os
import time
import requests
import asyncio
from telegram import Bot
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv("config.env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL_MONITOR = f"https://coinmarketcap.com/pt-br/currencies/pepe-coin-bsc2/"
bot = Bot(token=TELEGRAM_TOKEN)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

def fetch_last_price():
    response = requests.get(URL_MONITOR, headers=HEADERS)

    if response.status_code != 200:
        print(f"Erro ao acessar >> {URL_MONITOR} << Status: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", {"class": "sc-b3fc6b7-0 dzgUIj"})
    content = content.getText()

    return content

def monitor_price():

    seen_prices = set()

    while True:
        price = fetch_last_price()

        if price not in seen_prices:
            seen_prices.add(price)
            asyncio.run(
                bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID, 
                    text=f"NOVO PREÇO DA PEPE COIN DETECTED >> {price}"
                )
            )
        print(f"SET STATE >> {seen_prices}")
        time.sleep(30)


if __name__ == "__main__":
    print(f"Monitorando preço na url  >> {URL_MONITOR}\n << ...")
    monitor_price()
