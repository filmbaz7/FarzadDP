# db_helper.py

discounts = []

def add_discount(name, link, price_was, price_is, discount_percent, image_url):
    discounts.append({
        "title": f"{name} - {discount_percent}% تخفیف",
        "link": link
    })

def get_discounts():
    return discounts[-10:]  # آخرین ۱۰ تخفیف

def add_user(user_id):
    pass  # در این نسخه نیازی نیست

def get_users():
    return []  # اگر لازم داشتی بعداً اضافه می‌کنیم
