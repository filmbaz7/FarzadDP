from flask import Flask, request
import logging
import requests
import os
from scraper_runner import run_spider
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def split_message(text, max_length=4000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

def send_message(chat_id, text):
    for chunk in split_message(text):
        res = requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": chunk}
        )
        if not res.ok:
            logger.error(f"❌ Failed to send message: {res.text}")

@app.route('/')
def index():
    return "✅ Bot is running!"

@app.route('/webhook', methods=["POST"])
def webhook():
    data = request.get_json()
    logger.info(f"📩 Received: {data}")

    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if text == "/start":
        send_message(chat_id, "⏳ در حال جستجوی تخفیف‌ها...")

        results = run_spider()

        if not results:
            send_message(chat_id, "❌ چیزی پیدا نشد با تخفیف بالای ۳۰٪")
        else:
            msg = "🎯 تخفیف‌های بالای ۳۰٪:\n\n"
            for item in results:
                msg += (
                    f"🛍️ {item['name']}\n"
                    f"💸 قیمت: {item['priceIs']}€ (قبل: {item['priceWas']}€)\n"
                    f"📉 تخفیف: {item['discount']}٪ ({round(item['difference'],2)}€)\n"
                    f"🔗 {item['link']}\n\n"
                )
            send_message(chat_id, msg)

    return "", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
