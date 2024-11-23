import os

DEBUG = True
SECRET_KEY = "your_secret_key"
UPLOAD_FOLDER = os.path.join(os.getcwd(), "static/uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# 업로드 폴더 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
