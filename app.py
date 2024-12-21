import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_pyfile("config.py")

# JSON 파일 경로
DATA_FILE = "data.json"

# 편지 데이터 로드 함수
def load_letters():
    """JSON 파일에서 편지 데이터를 로드"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 편지 데이터 저장 함수
def save_letters(letters):
    """편지 데이터를 JSON 파일에 저장"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(letters, f, ensure_ascii=False, indent=4)

# 새 편지 추가 함수
def save_letter(letter):
    """새 편지를 JSON 파일에 추가"""
    letters = load_letters()
    letter["id"] = letters[-1]["id"] + 1 if letters else 1  # ID 생성
    letters.append(letter)
    save_letters(letters)

@app.route("/")
def home():
    """첫 페이지: 편지 목록"""
    letters = load_letters()
    return render_template("index.html", letters=letters)

@app.route("/write", methods=["GET", "POST"])
def write():
    """편지 작성 페이지"""
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")
        file = request.files.get("image")

        if not name or not message:
            flash("이름과 내용을 입력해야 합니다!", "error")
            return redirect(url_for("write"))

        # 파일 업로드 처리
        image_filename = None
        if file and file.filename:
            image_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))

        # 새 편지 생성
        letter = {
            "name": name,
            "message": message,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "image": image_filename,
        }
        save_letter(letter)
        flash("편지가 성공적으로 게시되었습니다!", "success")
        return redirect(url_for("home"))

    return render_template("write.html")

@app.route('/add', methods=['POST'])
def add_letter():
    """새 편지 추가 API"""
    name = request.form["name"]
    date = request.form["date"]
    message = request.form["message"]

    new_letter = {
        "name": name,
        "date": date,
        "message": message,
        "image": None,  # 이미지 처리 추가 가능
    }
    save_letter(new_letter)
    return redirect(url_for("home"))

@app.route('/delete/<int:letter_id>', methods=['DELETE'])
def delete_letter(letter_id):
    """편지 삭제 API"""
    letters = load_letters()
    # 해당 ID의 편지 삭제
    letters = [letter for letter in letters if letter['id'] != letter_id]
    save_letters(letters)
    return jsonify({"message": "편지가 삭제되었습니다."}), 200

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", message="Page not found"), 404

if __name__ == "__main__":
    app.run(debug=True)
