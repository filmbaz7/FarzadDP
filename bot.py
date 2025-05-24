from flask import Flask, request
import logging
import requests
import os
from scraper_runner import run_spider
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

if not TELEGRAM_TOKEN:
    raise ValueError("❌ توکن تلگرام پیدا نشد. لطفاً آن را در فایل .env تعریف کن.")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# تقسیم متن به تکه‌های زیر 4000 کاراکتر (حداکثر طول پیام تلگرام)
def split_message(text, max_length=4000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

# ارسال پیام به تلگرام
def send_message(chat_id, text):
    for chunk in split_message(text):
        res = requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": chunk}
        )
        if not res.ok:
            logger.error(f"❌ ارسال پیام ناموفق بود: {res.text}")

# تست سلامت سرور
@app.route('/')
def index():
    return "✅ ربات فعال است!"

# Webhook برای دریافت پیام تلگرام
@app.route('/webhook', methods=["POST"])
def webhook():
    data = request.get_json()
    logger.info(f"📩 پیام دریافتی: {data}")

    message = data.get("message")
    if not message:
        return "No message found", 200

    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if not chat_id:
        logger.warning("⚠️ chat_id پیدا نشد.")
        return "No chat_id", 200

    if text.strip() == "/start":
        send_message(chat_id, "⏳ در حال جستجوی تخفیف‌های بالای ۳۰٪ ...")

        results = run_spider()

        if not results:
            send_message(chat_id, "❌ تخفیفی بالای ۳۰٪ پیدا نشد.")
        else:
            msg = "🎯 تخفیف‌های بالای ۳۰٪:\n\n"
            for item in results:
                msg += (
                    f"🛍️ {item.get('name', '-')}\n"
                    f"💸 قیمت: {item.get('priceIs', '?')}€ (قبل: {item.get('priceWas', '?')}€)\n"
                    f"📉 تخفیف: {item.get('discount', '?')}٪ (حدود {round(item.get('difference', 0), 2)}€)\n"
                    f"🔗 {item.get('link', '-')}\n\n"
                )
            send_message(chat_id, msg)

    else:
        send_message(chat_id, "🤖 برای شروع، دستور /start را ارسال کنید.")

    return "", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
