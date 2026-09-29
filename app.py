from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from flask_jwt_extended import JWTManager

from config import (
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
    JWT_SECRET_KEY,
    CA_PATH
)

from db import db

from routes.auth import auth_bp
from routes.notes import notes_bp
from routes.files import files_bp
from routes.search import search_bp
from routes.ask import ask_bp
from routes.ai_queries import ai_queries_bp
from routes.chat_history import chat_history_bp


# =========================================================
# CREATE FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# CORS CONFIGURATION
# =========================================================
#
# Frontend:
#   http://localhost:5173
#   http://127.0.0.1:5173
#
# Backend:
#   http://127.0.0.1:5000
#
# Authorization header is allowed because
# protected APIs use JWT.
# =========================================================

CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173"
            ],
            "methods": [
                "GET",
                "POST",
                "PUT",
                "DELETE",
                "OPTIONS"
            ],
            "allow_headers": [
                "Content-Type",
                "Authorization"
            ]
        }
    }
)


# =========================================================
# EXTRA CORS RESPONSE HEADERS
# =========================================================
#
# This makes sure that the actual API response,
# including error responses such as HTTP 500,
# contains the required CORS headers.
# =========================================================

@app.after_request
def add_cors_headers(response):

    origin = request.headers.get("Origin")

    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]

    if origin in allowed_origins:

        response.headers["Access-Control-Allow-Origin"] = origin

        response.headers["Access-Control-Allow-Headers"] = (
            "Content-Type, Authorization"
        )

        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, DELETE, OPTIONS"
        )

    return response


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

app.config["SQLALCHEMY_DATABASE_URI"] = (
    SQLALCHEMY_DATABASE_URI
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
    SQLALCHEMY_TRACK_MODIFICATIONS
)

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {

    "connect_args": {

        "ssl_verify_cert": True,

        "ssl_verify_identity": True,

        "ssl_ca": CA_PATH

    }

}


# =========================================================
# JWT CONFIGURATION
# =========================================================

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY


# =========================================================
# INITIALIZE DATABASE
# =========================================================

db.init_app(app)


# =========================================================
# INITIALIZE JWT
# =========================================================

jwt = JWTManager(app)


# =========================================================
# SWAGGER CONFIGURATION
# =========================================================

app.config["SWAGGER"] = {

    "title": "AI Knowledge Assistant API",

    "description": (
        "Backend API for AI Knowledge Assistant"
    ),

    "version": "1.0.0",

    "doc_expansion": "list",

    "ui_params": {

        "displayOperationId": True,

        "persistAuthorization": True

    },

    "ui_params_text": """
    {
        "operationsSorter": function(a, b) {

            var order = {

                "POST /auth/register": 1,
                "POST /auth/login": 2,
                "GET /auth/profile": 3,

                "POST /notes": 4,
                "GET /notes": 5,
                "GET /notes/{note_id}": 6,
                "PUT /notes/{note_id}": 7,
                "DELETE /notes/{note_id}": 8,

                "POST /files/upload": 9,
                "GET /files/{document_id}/text": 10,
                "GET /files/{document_id}/chunks": 11,
                "POST /files/{document_id}/embed": 12,
                "DELETE /files/{document_id}/vector": 13,

                "POST /search": 14,

                "POST /ask": 15,

                "GET /ai-queries": 16,

                "GET /chat-history": 17

            };

            var keyA =
                a.get("method").toUpperCase()
                + " "
                + a.get("path");

            var keyB =
                b.get("method").toUpperCase()
                + " "
                + b.get("path");

            var positionA =
                order[keyA] || 999;

            var positionB =
                order[keyB] || 999;

            return positionA - positionB;
        },

        "tagsSorter": function(a, b) {

            var order = {

                "Authentication": 1,
                "Notes": 2,
                "Files": 3,
                "Search": 4,
                "Ask": 5,
                "AI Queries": 6,
                "Chat History": 7

            };

            var positionA =
                order[a] || 999;

            var positionB =
                order[b] || 999;

            return positionA - positionB;
        }
    }
    """
}


# =========================================================
# SWAGGER SPEC CONFIGURATION
# =========================================================

swagger_config = {

    "headers": [],

    "specs": [

        {

            "endpoint": "swagger",

            "route": "/swagger.json",

            "rule_filter": lambda rule: (

                rule.rule.startswith("/auth")

                or rule.rule == "/notes"

                or rule.rule.startswith("/notes/")

                or rule.rule.startswith("/files/")

                or rule.rule.startswith("/search")

                or rule.rule.startswith("/ask")

                or rule.rule.startswith("/ai-queries")

                or rule.rule.startswith("/chat-history")

            ),

            "model_filter": lambda tag: True,

            "static_url_path": "/flasgger_static",

            "swagger_ui": True,

            "specs_route": "/apidocs/"

        }

    ],

    "static_url_path": "/flasgger_static",

    "swagger_ui": True,

    "specs_route": "/apidocs/"

}


# =========================================================
# SWAGGER TEMPLATE
# =========================================================

swagger_template = {

    "swagger": "2.0",

    "info": {

        "title": "AI Knowledge Assistant API",

        "description": (
            "Backend API for AI Knowledge Assistant"
        ),

        "version": "1.0.0"

    },

    "securityDefinitions": {

        "Bearer": {

            "type": "apiKey",

            "name": "Authorization",

            "in": "header",

            "description": (
                "Enter: Bearer <your JWT token>"
            )

        }

    },

    "tags": [

        {

            "name": "Authentication",

            "description": (
                "User authentication APIs"
            )

        },

        {

            "name": "Notes",

            "description": (
                "Notes management APIs"
            )

        },

        {

            "name": "Files",

            "description": (
                "File upload and document processing APIs"
            )

        },

        {

            "name": "Search",

            "description": (
                "Semantic document search APIs"
            )

        },

        {

            "name": "Ask",

            "description": (
                "AI question answering using RAG"
            )

        },

        {

            "name": "AI Queries",

            "description": (
                "Previously asked AI questions"
            )

        },

        {

            "name": "Chat History",

            "description": (
                "AI responses and confidence scores"
            )

        }

    ]

}


# =========================================================
# INITIALIZE SWAGGER
# =========================================================

swagger = Swagger(
    app,
    config=swagger_config,
    template=swagger_template
)


# =========================================================
# REGISTER BLUEPRINTS
# =========================================================

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

app.register_blueprint(
    ai_queries_bp
)

app.register_blueprint(
    chat_history_bp
)


# =========================================================
# HOME
# =========================================================

@app.route(
    "/",
    methods=["GET"]
)
def home():

    return jsonify({

        "message":
            "AI Knowledge Assistant Backend is running"

    })


# =========================================================
# TEST DATABASE
# =========================================================

@app.route(
    "/test-db",
    methods=["GET"]
)
def test_db():

    try:

        from sqlalchemy import text

        db.session.execute(
            text("SELECT 1")
        )

        return jsonify({

            "message":
                "Database connected successfully"

        })

    except Exception as e:

        return jsonify({

            "error":
                str(e)

        }), 500


# =========================================================
# SHOW ROUTES
# =========================================================

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

            "methods":
                sorted(
                    method
                    for method in rule.methods
                    if method not in [
                        "HEAD",
                        "OPTIONS"
                    ]
                ),

            "path":
                str(rule)

        })

    return jsonify(routes)


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    print(
        "==========================================",
        flush=True
    )

    print(
        "AI KNOWLEDGE ASSISTANT BACKEND",
        flush=True
    )

    print(
        "==========================================",
        flush=True
    )

    print(
        "Backend: http://127.0.0.1:5000",
        flush=True
    )

    print(
        "Frontend: http://localhost:5173",
        flush=True
    )

    print(
        "CORS: Enabled",
        flush=True
    )

    print(
        "==========================================",
        flush=True
    )

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
