import os

from dotenv import load_dotenv


# ============================================================
# LOAD .ENV
# ============================================================

load_dotenv()


# ============================================================
# MYSQL CONFIGURATION
# ============================================================

MYSQL_HOST = os.getenv(
    "MYSQL_HOST",
    "localhost"
)

MYSQL_USER = os.getenv(
    "MYSQL_USER",
    "root"
)

MYSQL_PASSWORD = os.getenv(
    "MYSQL_PASSWORD",
    ""
)

MYSQL_DB = os.getenv(
    "MYSQL_DB",
    "ai_knowledge_db"
)


# ============================================================
# SQLALCHEMY DATABASE URI
# ============================================================

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://"
    f"{MYSQL_USER}:"
    f"{MYSQL_PASSWORD}@"
    f"{MYSQL_HOST}/"
    f"{MYSQL_DB}"
)


# ============================================================
# SQLALCHEMY
# ============================================================

SQLALCHEMY_TRACK_MODIFICATIONS = False


# ============================================================
# JWT
# ============================================================

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY"
)


# ============================================================
# GEMINI
# ============================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)