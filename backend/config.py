import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", 3306)
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME", "blog")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 1 day

    UPLOAD_FOLDER = "/app/uploads"
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

    BLOG_START_DATE = os.getenv("BLOG_START_DATE", "2025-01-01")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
