import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_pyfile("config.py")

DATABASE = "letters.db"

# 데이터베이스 연결 함수
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# 데이터베이스 초기화 함수
def initialize_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE letter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL,
                date TEXT NOT NULL,
                image TEXT
            )
        ''')
        conn.commit()
        conn.close()

# 앱 시작 시 데이터베이스 초기화
initialize_db()

@app.route("/")
def home():
    """첫 페이지: 편지 목록"""
    conn = get_db_connection()
    letters = conn.execute("SELECT * FROM letter ORDER BY id DESC").fetchall()
    conn.close()
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

        # 데이터베이스에 새 편지 추가
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO letter (name, message, date, image) VALUES (?, ?, ?, ?)",
            (name, message, datetime.now().strftime("%Y-%m-%d %H:%M"), image_filename),
        )
        conn.commit()
        conn.close()

        flash("편지가 성공적으로 게시되었습니다!", "success")
        return redirect(url_for("home"))

    return render_template("write.html")

@app.route('/delete/<int:letter_id>', methods=['DELETE'])
def delete_letter(letter_id):
    """편지 삭제 API"""
    conn = get_db_connection()
    conn.execute("DELETE FROM letter WHERE id = ?", (letter_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "편지가 삭제되었습니다."}), 200

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", message="Page not found"), 404

if __name__ == "__main__":
    app.run(debug=True)
