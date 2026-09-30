# -*- coding: utf-8 -*-
import unittest
from app import app, BOOKS


class LibraryMSTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    # 1. Kiểm tra danh sách BOOKS >= 4 cuốn và đủ các trường
    def test_books_dataset(self):
        self.assertGreaterEqual(len(BOOKS), 4, "BOOKS phải có ít nhất 4 cuốn")
        required_fields = {"id", "title", "author", "year", "category", "available"}
        for book in BOOKS:
            self.assertTrue(
                required_fields.issubset(book.keys()),
                f"Cuốn sách ID {book.get('id')} thiếu các trường bắt buộc",
            )
            self.assertIsInstance(book["id"], int)
            self.assertIsInstance(book["title"], str)
            self.assertIsInstance(book["author"], str)
            self.assertIsInstance(book["year"], int)
            self.assertIsInstance(book["category"], str)
            self.assertIsInstance(book["available"], bool)

    # 2. Kiểm tra Route / : tổng số đầu sách, số sách sẵn sàng cho mượn
    def test_route_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)

        total_books = len(BOOKS)
        available_books = sum(1 for b in BOOKS if b["available"])

        self.assertIn(str(total_books), data)
        self.assertIn(str(available_books), data)
        self.assertIn("Tổng số đầu sách", data)
        self.assertIn("sẵn sàng cho mượn", data)

    # 3. Kiểm tra Route /books : bảng sách, liên kết chi tiết, lọc ?category=Lập trình
    def test_route_books_all(self):
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)

        # Kiểm tra hiển thị đủ các sách
        for book in BOOKS:
            self.assertIn(book["title"], data)
            self.assertIn(f"/books/{book['id']}", data)

        # Kiểm tra thanh lọc thể loại
        self.assertIn("Thể loại", data)
        self.assertIn("Lập trình", data)

    def test_route_books_filter_category(self):
        # Lọc thể loại Lập trình
        response = self.client.get("/books?category=Lập trình")
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)

        # Sách thuộc Lập trình phải xuất hiện
        programming_books = [b for b in BOOKS if b["category"] == "Lập trình"]
        non_programming_books = [b for b in BOOKS if b["category"] != "Lập trình"]

        for book in programming_books:
            self.assertIn(book["title"], data)

        for book in non_programming_books:
            self.assertNotIn(f"<td>{book['title']}</td>", data)

    # 4. Kiểm tra Route /books/<int:book_id> : chi tiết & 404 khi không tồn tại
    def test_route_book_detail_success(self):
        response = self.client.get("/books/1")
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
        book1 = next(b for b in BOOKS if b["id"] == 1)
        self.assertIn(book1["title"], data)
        self.assertIn(book1["author"], data)
        self.assertIn(str(book1["year"]), data)

    def test_route_book_detail_404(self):
        # Không tồn tại -> 404 "Không có sách với ID = ..."
        response = self.client.get("/books/9999")
        self.assertEqual(response.status_code, 404)
        data = response.get_data(as_text=True)
        self.assertIn("Không có sách với ID = 9999", data)
        # Trang 404 có menu chung
        self.assertIn("<nav>", data)
        self.assertIn('href="/"', data)
        self.assertIn('href="/books"', data)

    # 5. Kiểm tra Route /api/books và /api/books/<int:book_id>
    def test_route_api_books(self):
        response = self.client.get("/api/books")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)
        self.assertEqual(len(json_data), len(BOOKS))

    def test_route_api_books_filter(self):
        response = self.client.get("/api/books?category=Lập trình")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(all(b["category"] == "Lập trình" for b in json_data))

    def test_route_api_book_detail_success(self):
        response = self.client.get("/api/books/1")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data["id"], 1)
        self.assertEqual(json_data["title"], BOOKS[0]["title"])

    def test_route_api_book_detail_404(self):
        # Không tồn tại -> {"error": "..."} với mã 404
        response = self.client.get("/api/books/9999")
        self.assertEqual(response.status_code, 404)
        json_data = response.get_json()
        self.assertIn("error", json_data)
        self.assertEqual(json_data["error"], "Không có sách với ID = 9999")

    # 6. Kiểm tra trang 404 tùy biến chung khi truy cập URL bất kỳ không tồn tại
    def test_generic_404_html(self):
        response = self.client.get("/duong-dan-khong-ton-tai")
        self.assertEqual(response.status_code, 404)
        data = response.get_data(as_text=True)
        self.assertIn("<nav>", data)
        self.assertIn("Lỗi 404", data)

    def test_generic_404_api(self):
        response = self.client.get("/api/khong-ton-tai")
        self.assertEqual(response.status_code, 404)
        json_data = response.get_json()
        self.assertIn("error", json_data)

    # 7. Kiểm tra HTML autoescaping dữ liệu chống XSS
    def test_html_autoescaping(self):
        malicious_book = {
            "id": 99999,
            "title": "<script>alert('XSS_ATTACK')</script>",
            "author": "<b>Hacker</b>",
            "year": 2026,
            "category": "Bảo mật",
            "available": True,
        }
        BOOKS.append(malicious_book)
        try:
            response = self.client.get("/books/99999")
            self.assertEqual(response.status_code, 200)
            data = response.get_data(as_text=True)
            self.assertNotIn("<script>alert('XSS_ATTACK')</script>", data)
            self.assertIn("&lt;script&gt;alert(&#39;XSS_ATTACK&#39;)&lt;/script&gt;", data)
            self.assertNotIn("<b>Hacker</b>", data)
            self.assertIn("&lt;b&gt;Hacker&lt;/b&gt;", data)
        finally:
            BOOKS.remove(malicious_book)


if __name__ == "__main__":
    unittest.main()
