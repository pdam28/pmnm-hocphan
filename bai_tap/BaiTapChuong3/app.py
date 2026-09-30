from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

# 1. Danh sách BOOKS >= 4 cuốn
BOOKS = [
    {
        "id": 1,
        "title": "Lập trình Python cơ bản",
        "author": "Nguyễn Văn A",
        "year": 2021,
        "category": "Lập trình",
        "available": True,
    },
    {
        "id": 2,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "year": 2008,
        "category": "Lập trình",
        "available": False,
    },
    {
        "id": 3,
        "title": "Dế Mèn phiêu lưu ký",
        "author": "Tô Hoài",
        "year": 1941,
        "category": "Văn học",
        "available": True,
    },
    {
        "id": 4,
        "title": "Vũ trụ trong vỏ hạt dẻ",
        "author": "Stephen Hawking",
        "year": 2001,
        "category": "Khoa học",
        "available": True,
    },
]


# 2. Trang chủ: tổng số đầu sách, số sách sẵn sàng cho mượn
@app.route("/")
def index():
    total_books = len(BOOKS)
    available_books = 0
    for book in BOOKS:
        if book["available"]:
            available_books += 1
    return render_template(
        "index.html", total_books=total_books, available_books=available_books
    )


# 3. Danh sách sách: lọc ?category=Lập trình và thanh lọc thể loại
@app.route("/books")
def book_list():
    category = request.args.get("category")
    if category:
        books = [b for b in BOOKS if b["category"] == category]
    else:
        books = BOOKS

    # Lấy các thể loại không trùng nhau
    categories = []
    for b in BOOKS:
        if b["category"] not in categories:
            categories.append(b["category"])

    return render_template(
        "books.html",
        books=books,
        categories=categories,
        selected_category=category,
    )


# 4. Chi tiết sách: không tồn tại -> 404 "Không có sách với ID = ..."
@app.route("/books/<int:book_id>")
def book_detail(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return render_template("book_detail.html", book=book)
    return render_template("404.html", message=f"Không có sách với ID = {book_id}"), 404


# 5. API trả về danh sách sách JSON
@app.route("/api/books")
def api_books():
    category = request.args.get("category")
    if category:
        books = [b for b in BOOKS if b["category"] == category]
        return jsonify(books)
    return jsonify(BOOKS)


# 5. API trả về chi tiết sách JSON: không tồn tại -> {"error": "..."} với mã 404
@app.route("/api/books/<int:book_id>")
def api_book_detail(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return jsonify(book)
    return jsonify({"error": f"Không có sách với ID = {book_id}"}), 404


# 6. Trang 404 tùy biến (phân biệt API và HTML)
@app.errorhandler(404)
def page_not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Không tìm thấy tài nguyên API"}), 404
    return render_template("404.html", message="Không tìm thấy trang"), 404


if __name__ == "__main__":
    app.run(debug=True)
