import os

from dotenv import load_dotenv


# ============================================================
# LOAD .ENV
# ============================================================

load_dotenv()


# ============================================================
# TIDB CONFIGURATION
# ============================================================

TIDB_HOST = os.getenv(
    "TIDB_HOST"
)

TIDB_PORT = int(os.getenv(
    "TIDB_PORT",
    "4000"
))

TIDB_USER = os.getenv(
    "TIDB_USER"
)

TIDB_PASSWORD = os.getenv(
    "TIDB_PASSWORD"
)

TIDB_DB_NAME = os.getenv(
    "TIDB_DB_NAME",
    "ai_knowledge_db"
)

CA_PATH = os.getenv(
    "CA_PATH"
)


# ============================================================
# SQLALCHEMY DATABASE URI
# ============================================================

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://"
    f"{TIDB_USER}:"
    f"{TIDB_PASSWORD}@"
    f"{TIDB_HOST}:"
    f"{TIDB_PORT}/"
    f"{TIDB_DB_NAME}"
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