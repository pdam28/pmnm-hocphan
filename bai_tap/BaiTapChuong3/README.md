# Bài Tập Dự Án: LibraryMS v0.1 · ★★ (Chương 3 · Flask Căn Bản)

Ứng dụng web Quản lý Thư viện đơn giản xây dựng bằng **Python** và **Flask**, sử dụng HTML thuần (không dùng CSS) theo đúng phong cách học phần lập trình căn bản, đáp ứng đầy đủ tất cả các yêu cầu và tiêu chí chấm điểm của bài tập.

---

## 📁 Cấu Trúc Thư Mục

```text
Chuong3/
└── BaiTapChuong3/
    ├── app.py                # Ứng dụng Flask chính (dữ liệu BOOKS, 5 route, error handler)
    ├── test_app.py           # Bộ kiểm thử tự động (13 test cases)
    ├── README.md             # Hướng dẫn sử dụng & tài liệu dự án
    └── templates/
        ├── base.html         # Layout khung sườn chung (Menu chung: Trang chủ | Danh sách | API)
        ├── index.html        # Trang chủ: Thống kê tổng số sách, sách sẵn sàng
        ├── books.html        # Trang bảng danh sách sách & thanh lọc thể loại
        ├── book_detail.html  # Trang chi tiết một cuốn sách
        └── 404.html          # Trang lỗi 404 tùy biến có menu chung
```

---

## 📋 Các Tính Năng Đã Hoàn Thiện Theo Yêu Cầu

### 1. Danh Sách `BOOKS` (≥ 4 cuốn)
Khai báo danh sách `BOOKS` trong `app.py` với các trường dữ liệu:
- `id` (int)
- `title` (str)
- `author` (str)
- `year` (int)
- `category` (str)
- `available` (bool: `True`/`False`)

### 2. Route `/` (Trang chủ)
- Hiển thị **tổng số đầu sách** trong thư viện.
- Hiển thị **số sách sẵn sàng cho mượn** (`available == True`).

### 3. Route `/books` (Danh mục & Lọc thể loại)
- Bảng HTML (`<table border="1">`): ID, Tên sách, Tác giả, Năm XB, Thể loại, Tình trạng (Sẵn sàng / Đã mượn).
- **Tên sách liên kết đến trang chi tiết**: Sử dụng `url_for('book_detail', book_id=book.id)`.
- **Thanh liên kết theo thể loại**: Danh sách các liên kết `Tất cả` và các thể loại như `Lập trình`, `Khoa học`, `Văn học`, v.v.
- Hỗ trợ lọc qua query parameter: `/books?category=Lập trình`.

### 4. Route `/books/<int:book_id>` (Chi tiết sách)
- Hiển thị toàn bộ thông tin chi tiết của cuốn sách tương ứng.
- Nếu `book_id` không tồn tại trong hệ thống: Trả về mã HTTP **404** cùng thông báo `"Không có sách với ID = <book_id>"`.

### 5. API RESTful `/api/books` & `/api/books/<int:book_id>`
- `GET /api/books`: Trả về danh sách sách dưới dạng **JSON** (hỗ trợ lọc `?category=...`).
- `GET /api/books/<int:book_id>`: Trả về **JSON** chi tiết cuốn sách.
- Nếu không tìm thấy: Trả về `{"error": "Không có sách với ID = <book_id>"}` với mã HTTP **404**.

### 6. Trang 404 Tùy Biến (Có Menu Chung)
- File `templates/404.html` kế thừa từ `templates/base.html`, có đầy đủ menu liên kết chung.
- Tự động phân biệt giữa yêu cầu Web (trả về HTML 404) và yêu cầu API (trả về JSON 404).

### 7. Dùng `url_for` & Escape Dữ Liệu
- Mọi liên kết đều dùng `url_for(...)`.
- Mọi dữ liệu chèn vào HTML đều được Jinja2 tự động escape chống XSS.

---

## 🚀 Hướng Dẫn Chạy Ứng Dụng

### Khởi động máy chủ Flask:
```powershell
.\.venv\Scripts\python.exe Chuong3/BaiTapChuong3/app.py
```
Truy cập: `http://127.0.0.1:5000/`

### Chạy kiểm thử tự động:
```powershell
& ".\.venv\Scripts\python.exe" Chuong3/BaiTapChuong3/test_app.py
```
