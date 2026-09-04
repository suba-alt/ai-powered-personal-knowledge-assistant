from flask import Blueprint, request, jsonify

import bcrypt

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from flasgger import swag_from

from db import db
from model import User


# =========================================================
# AUTH BLUEPRINT
# =========================================================

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# =========================================================
# REGISTER USER
# =========================================================

@auth_bp.route("/register", methods=["POST"])
@swag_from({

    "tags": [
        "Authentication"
    ],

    "summary": "Register User",

    "description": (
        "Create a new user account."
    ),

    "operationId": "registerUser",

    "consumes": [
        "application/json"
    ],

    "produces": [
        "application/json"
    ],

    "parameters": [

        {

            "name": "body",

            "in": "body",

            "required": True,

            "schema": {

                "type": "object",

                "required": [
                    "name",
                    "email",
                    "password"
                ],

                "properties": {

                    "name": {

                        "type": "string",

                        "example": "Suba"
                    },

                    "email": {

                        "type": "string",

                        "example": "suba@gmail.com"
                    },

                    "password": {

                        "type": "string",

                        "example": "password123"
                    }
                }
            }
        }
    ],

    "responses": {

        "201": {

            "description": (
                "User registered successfully"
            ),

            "examples": {

                "application/json": {

                    "message":
                    "User registered successfully"
                }
            }
        },

        "400": {

            "description":
            "Request body or fields are missing"
        },

        "409": {

            "description":
            "Email already registered"
        },

        "500": {

            "description":
            "Registration failed"
        }
    }
})
def register():

    data = request.get_json()


    if not data:

        return jsonify({

            "message":
            "Request body is required"

        }), 400


    name = data.get("name")

    email = data.get("email")

    password = data.get("password")


    if not name or not email or not password:

        return jsonify({

            "message":
            "Name, email and password are required"

        }), 400


    existing_user = User.query.filter_by(
        email=email
    ).first()


    if existing_user:

        return jsonify({

            "message":
            "Email already registered"

        }), 409


    hashed_password = bcrypt.hashpw(

        password.encode("utf-8"),

        bcrypt.gensalt()

    ).decode("utf-8")


    user = User(

        name=name,

        email=email,

        password=hashed_password
    )


    try:

        db.session.add(user)

        db.session.commit()


        return jsonify({

            "message":
            "User registered successfully"

        }), 201


    except Exception as e:

        db.session.rollback()


        return jsonify({

            "message":
            "Registration failed",

            "error": str(e)

        }), 500


# =========================================================
# LOGIN USER
# =========================================================

@auth_bp.route("/login", methods=["POST"])
@swag_from({

    "tags": [
        "Authentication"
    ],

    "summary": "Login User",

    "description": (
        "Login using email and password."
    ),

    "operationId": "loginUser",

    "consumes": [
        "application/json"
    ],

    "produces": [
        "application/json"
    ],

    "parameters": [

        {

            "name": "body",

            "in": "body",

            "required": True,

            "schema": {

                "type": "object",

                "required": [
                    "email",
                    "password"
                ],

                "properties": {

                    "email": {

                        "type": "string",

                        "example":
                        "suba@gmail.com"
                    },

                    "password": {

                        "type": "string",

                        "example":
                        "password123"
                    }
                }
            }
        }
    ],

    "responses": {

        "200": {

            "description":
            "Login successful",

            "examples": {

                "application/json": {

                    "message":
                    "Login successful",

                    "access_token":
                    "your_jwt_token",

                    "user": {

                        "id": 1,

                        "name": "Suba",

                        "email":
                        "suba@gmail.com"
                    }
                }
            }
        },

        "400": {

            "description":
            "Email and password are required"
        },

        "401": {

            "description":
            "Invalid email or password"
        }
    }
})
def login():

    data = request.get_json()


    if not data:

        return jsonify({

            "message":
            "Request body is required"

        }), 400


    email = data.get("email")

    password = data.get("password")


    if not email or not password:

        return jsonify({

            "message":
            "Email and password are required"

        }), 400


    user = User.query.filter_by(
        email=email
    ).first()


    if not user:

        return jsonify({

            "message":
            "Invalid email or password"

        }), 401


    password_valid = bcrypt.checkpw(

        password.encode("utf-8"),

        user.password.encode("utf-8")
    )


    if not password_valid:

        return jsonify({

            "message":
            "Invalid email or password"

        }), 401


    access_token = create_access_token(

        identity=str(user.id)
    )


    return jsonify({

        "message":
        "Login successful",

        "access_token":
        access_token,

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email
        }

    }), 200


# =========================================================
# GET USER PROFILE
# =========================================================

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
@swag_from({

    "tags": [
        "Authentication"
    ],

    "summary": "Get User Profile",

    "description": (
        "Get the profile of the "
        "currently authenticated user."
    ),

    "operationId":
    "getUserProfile",

    "produces": [
        "application/json"
    ],

    "security": [

        {
            "Bearer": []
        }
    ],

    "parameters": [

        {

            "name":
            "Authorization",

            "in":
            "header",

            "type":
            "string",

            "required":
            True,

            "description": (
                "JWT authorization header. "
                "Format: Bearer "
                "<your_access_token>"
            ),

            "example":
            "Bearer eyJhbGciOiJIUzI1NiIs..."
        }
    ],

    "responses": {

        "200": {

            "description":
            "User profile",

            "examples": {

                "application/json": {

                    "id": 1,

                    "name": "Suba",

                    "email":
                    "suba@gmail.com"
                }
            }
        },

        "401": {

            "description":
            "Missing or invalid JWT token"
        },

        "404": {

            "description":
            "User not found"
        }
    }
})
def profile():

    user_id = get_jwt_identity()


    user = User.query.get(user_id)


    if not user:

        return jsonify({

            "message":
            "User not found"

        }), 404


    return jsonify({

        "id": user.id,

        "name": user.name,

        "email": user.email

    }), 200