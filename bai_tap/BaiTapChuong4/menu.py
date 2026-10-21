from datetime import datetime
from math import ceil
from flask import Flask, render_template, request, abort

SHOP = {
    "name": "Cà phê Sông Hương",
    "address": "12 Lê Lợi, Huế",
    "phone": "0234 3888 999",
    "open": 7,
    "close": 22
}

PROMOTION = [
    "Giảm 10% cho sinh viên",
    "Mua 2 tặng 1 vào thứ Hai"
]

# Danh sách 7 món phục vụ phân trang (3 món/trang -> 3 trang)
MENU = [
    {"name": "Cà phê đen", "price": 20000, "available": True},
    {"name": "Cà phê sữa", "price": 25000, "available": True},
    {"name": "Bạc xỉu", "price": 30000, "available": False},
    {"name": "Trà đào", "price": 35000, "available": True},
    {"name": "Trà sữa", "price": 40000, "available": True},
    {"name": "Nước cam", "price": 30000, "available": True},
    {"name": "Sinh tố bơ", "price": 45000, "available": True}
]

app = Flask(__name__)


# Filter định dạng tiền tệ Việt Nam (Ví dụ: 25000 -> 25.000 đ)
@app.template_filter("vnd")
def vnd(value):
    return f"{int(value):,} đ".replace(",", ".")


@app.route("/")
def index():
    hour = request.args.get("gio", type=int)
    if hour is None or not (0 <= hour <= 23):
        hour = datetime.now().hour
    is_open = SHOP["open"] <= hour < SHOP["close"]
    return render_template(
        "index.html",
        shop=SHOP,
        hour=hour,
        is_open=is_open,
        promotions=PROMOTION
    )


@app.route("/menu")
def index_menu():
    page = request.args.get("page", 1, type=int)
    per_page = 3
    total = len(MENU)
    pages = max(1, ceil(total / per_page))

    # Nếu trang nhỏ hơn 1 hoặc lớn hơn tổng số trang thì báo lỗi 404
    if page < 1 or page > pages:
        abort(404)

    start = (page - 1) * per_page
    current_items = MENU[start:start + per_page]
    avg_price = sum(item["price"] for item in MENU) / total if total else 0
    available_count = sum(1 for item in MENU if item["available"])

    return render_template(
        "index_menu.html",
        menu=current_items,
        page=page,
        pages=pages,
        total=total,
        avg_price=avg_price,
        available_count=available_count
    )


@app.route("/contact")
def contact():
    return render_template("contact.html", shop=SHOP)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
