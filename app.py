import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_pyfile("config.py")

# 편지 데이터를 JSON 파일로 저장
DATA_FILE = "data.json"

def load_letters():
    """JSON 파일에서 편지 데이터를 로드"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_letter(letter):
    """새 편지를 JSON 파일에 추가"""
    letters = load_letters()
    letters.append(letter)
    with open(DATA_FILE, "w") as f:
        json.dump(letters, f, indent=4)

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", message="Page not found"), 404

if __name__ == "__main__":
    app.run(debug=True)
