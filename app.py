from flask import (
    Flask,
    jsonify
)

from config import (
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
    JWT_SECRET_KEY
)

from db import db

from flask_jwt_extended import JWTManager

from routes.auth import auth_bp
from routes.notes import notes_bp
from routes.files import files_bp
from routes.search import search_bp
from routes.ask import ask_bp


# ============================================================
# CREATE FLASK APPLICATION
# ============================================================

app = Flask(
    __name__
)


# ============================================================
# SQLALCHEMY CONFIGURATION
# ============================================================

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = SQLALCHEMY_DATABASE_URI


app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = SQLALCHEMY_TRACK_MODIFICATIONS


# ============================================================
# JWT CONFIGURATION
# ============================================================

app.config[
    "JWT_SECRET_KEY"
] = JWT_SECRET_KEY


# ============================================================
# INITIALIZE DATABASE
# ============================================================

db.init_app(
    app
)


# ============================================================
# INITIALIZE JWT
# ============================================================

jwt = JWTManager(
    app
)


# ============================================================
# REGISTER BLUEPRINTS
# ============================================================

app.register_blueprint(
    auth_bp
)

app.register_blueprint(
    notes_bp
)

app.register_blueprint(
    files_bp
)

app.register_blueprint(
    search_bp
)

app.register_blueprint(
    ask_bp
)


# ============================================================
# HOME
# ============================================================

@app.route(
    "/",
    methods=["GET"]
)
def home():

    return (
        "AI Knowledge Assistant "
        "Backend is Running!"
    )


# ============================================================
# DATABASE TEST
# ============================================================

@app.route(
    "/test-db",
    methods=["GET"]
)
def test_db():

    try:

        db.session.execute(
            db.text(
                "SELECT 1"
            )
        )

        return (
            "SQLAlchemy + MySQL "
            "connection successful!"
        )


    except Exception as e:

        return jsonify({

            "message":
                "Database connection failed",

            "error":
                str(e)

        }), 500


# ============================================================
# REGISTERED ROUTES TEST
# ============================================================

@app.route(
    "/routes",
    methods=["GET"]
)
def show_routes():

    routes = []

    for rule in app.url_map.iter_rules():

        routes.append({

            "endpoint":
                rule.endpoint,

            "url":
                str(rule),

            "methods":
                sorted(
                    rule.methods
                )

        })

    return jsonify(
        routes
    ), 200


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print()
    print(
        "=========================================="
    )

    print(
        "AI Knowledge Assistant Backend"
    )

    print(
        "=========================================="
    )

    print()

    print(
        "Registered routes:"
    )

    for rule in app.url_map.iter_rules():

        print(
            f"{str(rule):35} "
            f"{sorted(rule.methods)}"
        )

    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )