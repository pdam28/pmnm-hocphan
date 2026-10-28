from flask import Flask, render_template, request

app = Flask(__name__)

def parse_num(val_str):
    """Chuyển chuỗi sang số thực, chấp nhận cả dấu phẩy thập phân."""
    if not val_str or not val_str.strip():
        return None, "Vui lòng nhập một số."
    try:
        return float(val_str.strip().replace(",", ".")), None
    except ValueError:
        return None, "Vui lòng nhập một số."

def format_num(val):
    """Rút gọn số nguyên (ví dụ: 8.0 -> 8; 2.5 -> 2.5)."""
    return int(val) if val.is_integer() else val

def validate_score(val_str):
    """Hàm kiểm tra điểm số dùng chung cho cả 3 cột điểm ở Bài 2."""
    score, err = parse_num(val_str)
    if err:
        return None, err
    if score < 0 or score > 10:
        return None, "Điểm phải từ 0 đến 10."
    return score, None

@app.route("/", methods=["GET", "POST"])
def index():
    # Xác định tab hiện tại (mặc định là bai1)
    active_tab = request.args.get("tab", "bai1")

    # Dữ liệu khởi tạo cho Bài 1
    b1 = {
        "a": "", "b": "", "op": "+",
        "errors": {"a": None, "b": None, "op": None},
        "result": None
    }

    # Dữ liệu khởi tạo cho Bài 2
    b2 = {
        "cc": "", "gk": "", "ck": "",
        "errors": {"cc": None, "gk": None, "ck": None},
        "result": None
    }

    # Dữ liệu khởi tạo cho Bài 3
    b3 = {
        "height": "", "weight": "",
        "errors": {"height": None, "weight": None},
        "result": None
    }

    if request.method == "POST":
        form_type = request.form.get("form_type", "bai1")
        active_tab = form_type

        # ==================== BÀI 1: MÁY TÍNH CƠ BẢN ====================
        if form_type == "bai1":
            b1["a"] = request.form.get("a", "")
            b1["b"] = request.form.get("b", "")
            b1["op"] = request.form.get("op", "+")

            a_val, b1["errors"]["a"] = parse_num(b1["a"])
            b_val, b1["errors"]["b"] = parse_num(b1["b"])

            if b1["op"] not in ["+", "-", "*", "/"]:
                b1["errors"]["op"] = "Phép toán không hợp lệ."

            if b1["errors"]["b"] is None and b1["op"] == "/" and b_val == 0:
                b1["errors"]["b"] = "Không thể chia cho 0."

            if not any(b1["errors"].values()):
                ops = {
                    "+": a_val + b_val,
                    "-": a_val - b_val,
                    "*": a_val * b_val,
                    "/": a_val / b_val
                }
                res = ops[b1["op"]]
                b1["result"] = f"{format_num(a_val)} {b1['op']} {format_num(b_val)} = {format_num(res)}"

        # ==================== BÀI 2: TÍNH ĐIỂM HỌC PHẦN ====================
        elif form_type == "bai2":
            b2["cc"] = request.form.get("cc", "")
            b2["gk"] = request.form.get("gk", "")
            b2["ck"] = request.form.get("ck", "")

            cc_val, b2["errors"]["cc"] = validate_score(b2["cc"])
            gk_val, b2["errors"]["gk"] = validate_score(b2["gk"])
            ck_val, b2["errors"]["ck"] = validate_score(b2["ck"])

            if not any(b2["errors"].values()):
                total = round(cc_val * 0.1 + gk_val * 0.3 + ck_val * 0.6, 1)
                if ck_val < 1:
                    b2["result"] = f"{total} · F (điểm thi dưới 1)"
                else:
                    if total >= 8.5:
                        letter = "A"
                    elif total >= 7.0:
                        letter = "B"
                    elif total >= 5.5:
                        letter = "C"
                    elif total >= 4.0:
                        letter = "D"
                    else:
                        letter = "F"
                    b2["result"] = f"{total} · {letter}"

        # ==================== BÀI 3: CHỈ SỐ BMI ====================
        elif form_type == "bai3":
            b3["height"] = request.form.get("height", "")
            b3["weight"] = request.form.get("weight", "")

            h_val, h_err = parse_num(b3["height"])
            w_val, w_err = parse_num(b3["weight"])

            if h_err:
                b3["errors"]["height"] = h_err
            elif 0 < h_val <= 2.5:
                b3["errors"]["height"] = "Giá trị phải từ 50 đến 250. (nhập mét thay vì cm)"
            elif h_val < 50 or h_val > 250:
                b3["errors"]["height"] = "Giá trị phải từ 50 đến 250."

            if w_err:
                b3["errors"]["weight"] = w_err
            elif w_val < 10 or w_val > 300:
                b3["errors"]["weight"] = "Giá trị phải từ 10 đến 300."

            if not any(b3["errors"].values()):
                h_meter = h_val / 100.0
                bmi = round(w_val / (h_meter ** 2), 1)

                if bmi < 18.5:
                    status, color = "Thiếu cân", "yellow"
                elif bmi < 23:
                    status, color = "Bình thường", "green"
                elif bmi < 25:
                    status, color = "Thừa cân", "yellow"
                else:
                    status, color = "Béo phì", "red"

                min_w = round(18.5 * (h_meter ** 2), 1)
                max_w = round(22.9 * (h_meter ** 2), 1)

                b3["result"] = {
                    "text": f"{bmi} · {status}",
                    "color": color,
                    "ideal": f"{min_w} – {max_w} kg"
                }

    return render_template(
        "index.html",
        active_tab=active_tab,
        b1=b1,
        b2=b2,
        b3=b3
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)