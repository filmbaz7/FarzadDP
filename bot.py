import os
from flask import Flask, request
import telegram
import threading
import time
import subprocess
from db_helper import init_db, add_user, get_users, get_discounts

TOKEN = '7578063108:AAFZGQydjiQJImIaSi3uwUmE2_EA9yATrgE'
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

init_db()

def run_spider_subprocess():
    try:
        subprocess.run(["python", "run_spider.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"خطا در اجرای اسپایدر: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if not update.message:
        return 'No message', 200

    chat_id = update.message.chat.id
    text = update.message.text.strip()

    add_user(chat_id)

    if text == '/start':
        bot.send_message(chat_id, "سلام! برای دریافت تخفیف‌ها دستور /discounts رو ارسال کن.")
    elif text == '/discounts':
        bot.send_message(chat_id, "در حال دریافت آخرین تخفیف‌ها، لطفاً چند لحظه صبر کنید...")

        try:
            thread = threading.Thread(target=run_spider_subprocess)
            thread.start()
            thread.join(timeout=30)

            discounts = get_discounts()
            if discounts:
                msg = "\n\n".join([f"{title}\n{link}" for title, link in discounts[:10]])
            else:
                msg = "تخفیفی پیدا نشد."
            bot.send_message(chat_id, msg)
        except Exception as e:
            bot.send_message(chat_id, f"خطا در دریافت تخفیف‌ها: {e}")
    else:
        bot.send_message(chat_id, "دستور نامعتبر است. از /start یا /discounts استفاده کن.")

    return 'OK'

def send_periodic_discounts():
    while True:
        time.sleep(180)
        try:
            run_spider_subprocess()
            users = get_users()
            discounts = get_discounts()
            if not discounts:
                continue
            msg = "\n\n".join([f"{title}\n{link}" for title, link in discounts[:5]])
            for user_id in users:
                try:
                    bot.send_message(user_id, msg)
                except Exception as e:
                    print(f"خطا در ارسال به {user_id}: {e}")
        except Exception as e:
            print(f"خطا در اجرای ارسال دوره‌ای: {e}")

if __name__ == '__main__':
    threading.Thread(target=send_periodic_discounts, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
