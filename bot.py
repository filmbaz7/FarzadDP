import os
from flask import Flask, request
import telegram
import threading
import time
from db_helper import init_db, add_user, get_users, get_discounts
from scraper_runner import run_spider  # فرض بر این است که این تابع Scrapy رو اجرا می‌کند

TOKEN = '7578063108:AAFZGQydjiQJImIaSi3uwUmE2_EA9yATrgE'
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

init_db()

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    add_user(chat_id)  # کاربر رو ذخیره می‌کنیم

    if text == '/start':
        bot.send_message(chat_id, "سلام! برای دریافت تخفیف‌ها روی /discounts بزن.")
    elif text == '/discounts':
        bot.send_message(chat_id, "در حال دریافت تخفیف‌ها، لطفا صبر کنید...")
        # اجرای اسپایدر و ذخیره تخفیف‌ها در DB
        run_spider()
        discounts = get_discounts()
        if discounts:
            msg = "\n\n".join([f"{title}\n{link}" for title, link in discounts])
        else:
            msg = "فعلاً تخفیفی موجود نیست."
        bot.send_message(chat_id, msg)
    else:
        bot.send_message(chat_id, "دستور نامشخص. لطفا /start یا /discounts را ارسال کنید.")

    return 'OK'

def send_periodic_discounts():
    while True:
        time.sleep(180)  # هر 3 دقیقه
        users = get_users()
        discounts = get_discounts()
        if not discounts:
            continue
        msg = "\n\n".join([f"{title}\n{link}" for title, link in discounts])
        for user_id in users:
            try:
                bot.send_message(user_id, msg)
            except Exception as e:
                print(f"خطا در ارسال پیام به {user_id}: {e}")

if __name__ == '__main__':
    # اجرای ترد برای ارسال تخفیف‌های دوره‌ای
    thread = threading.Thread(target=send_periodic_discounts, daemon=True)
    thread.start()

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
