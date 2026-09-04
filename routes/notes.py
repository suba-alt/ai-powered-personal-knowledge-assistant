from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from flasgger import swag_from

from db import db
from model import Note


# ==================================================
# NOTES BLUEPRINT
# ==================================================

notes_bp = Blueprint(
    "notes",
    __name__,
    url_prefix="/notes"
)


# ==================================================
# CREATE NOTE
# POST /notes
# ==================================================

@notes_bp.route("", methods=["POST"])
@jwt_required()
@swag_from({

    "tags": [
        "Notes"
    ],

    "summary": "Create Note",

    "description": (
        "Create a new note for the logged-in user."
    ),

    "operationId": "createNote",

    "consumes": [
        "application/json"
    ],

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
            "name": "body",

            "in": "body",

            "required": True,

            "schema": {

                "type": "object",

                "required": [
                    "title",
                    "content"
                ],

                "properties": {

                    "title": {
                        "type": "string",
                        "example": "Python Notes"
                    },

                    "content": {
                        "type": "string",
                        "example": (
                            "Python is a "
                            "high-level programming language."
                        )
                    }
                }
            }
        }
    ],

    "responses": {

        "201": {

            "description":
            "Note created successfully",

            "examples": {

                "application/json": {

                    "message":
                    "Note created successfully",

                    "note": {

                        "id": 1,

                        "user_id": 1,

                        "title":
                        "Python Notes",

                        "content":
                        "Python is a high-level programming language."
                    }
                }
            }
        },

        "400": {

            "description":
            "Request body or required fields are missing"
        },

        "401": {

            "description":
            "Missing or invalid JWT token"
        },

        "500": {

            "description":
            "Failed to create note"
        }
    }
})
def create_note():

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "Request body is required"
        }), 400

    title = data.get("title")

    content = data.get("content")

    if not title or not content:

        return jsonify({
            "message":
            "Title and content are required"
        }), 400

    # Get logged-in user's ID
    user_id = get_jwt_identity()

    note = Note(

        user_id=int(user_id),

        title=title,

        content=content
    )

    try:

        db.session.add(note)

        db.session.commit()

        return jsonify({

            "message":
            "Note created successfully",

            "note": {

                "id": note.id,

                "user_id": note.user_id,

                "title": note.title,

                "content": note.content,

                "created_at": note.created_at,

                "updated_at": note.updated_at
            }

        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({

            "message":
            "Failed to create note",

            "error": str(e)

        }), 500


# ==================================================
# VIEW ALL NOTES
# GET /notes
# ==================================================

@notes_bp.route("", methods=["GET"])
@jwt_required()
@swag_from({

    "tags": [
        "Notes"
    ],

    "summary": "Get All Notes",

    "description": (
        "Get all notes belonging to "
        "the logged-in user."
    ),

    "operationId": "getAllNotes",

    "produces": [
        "application/json"
    ],

    "security": [
        {
            "Bearer": []
        }
    ],

    "responses": {

        "200": {

            "description":
            "Notes retrieved successfully"
        },

        "401": {

            "description":
            "Missing or invalid JWT token"
        }
    }
})
def get_notes():

    user_id = get_jwt_identity()

    notes = Note.query.filter_by(

        user_id=int(user_id)

    ).order_by(

        Note.created_at.desc()

    ).all()

    notes_list = []

    for note in notes:

        notes_list.append({

            "id": note.id,

            "user_id": note.user_id,

            "title": note.title,

            "content": note.content,

            "created_at": note.created_at,

            "updated_at": note.updated_at
        })

    return jsonify({

        "message":
        "Notes retrieved successfully",

        "notes":
        notes_list

    }), 200


# ==================================================
# VIEW ONE NOTE
# GET /notes/<note_id>
# ==================================================

@notes_bp.route("/<int:note_id>", methods=["GET"])
@jwt_required()
@swag_from({

    "tags": [
        "Notes"
    ],

    "summary": "Get Single Note",

    "description": (
        "Get one note belonging to "
        "the logged-in user."
    ),

    "operationId": "getSingleNote",

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
            "note_id",

            "in":
            "path",

            "type":
            "integer",

            "required":
            True,

            "example":
            1
        }
    ],

    "responses": {

        "200": {

            "description":
            "Note retrieved successfully"
        },

        "401": {

            "description":
            "Missing or invalid JWT token"
        },

        "404": {

            "description":
            "Note not found"
        }
    }
})
def get_note(note_id):

    user_id = get_jwt_identity()

    note = Note.query.filter_by(

        id=note_id,

        user_id=int(user_id)

    ).first()

    if not note:

        return jsonify({

            "message":
            "Note not found"

        }), 404

    return jsonify({

        "id": note.id,

        "user_id": note.user_id,

        "title": note.title,

        "content": note.content,

        "created_at": note.created_at,

        "updated_at": note.updated_at

    }), 200


# ==================================================
# UPDATE NOTE
# PUT /notes/<note_id>
# ==================================================

@notes_bp.route("/<int:note_id>", methods=["PUT"])
@jwt_required()
@swag_from({

    "tags": [
        "Notes"
    ],

    "summary": "Update Note",

    "description": (
        "Update an existing note belonging "
        "to the logged-in user."
    ),

    "operationId": "updateNote",

    "consumes": [
        "application/json"
    ],

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
            "note_id",

            "in":
            "path",

            "type":
            "integer",

            "required":
            True,

            "example":
            1
        },

        {

            "name":
            "body",

            "in":
            "body",

            "required":
            True,

            "schema": {

                "type":
                "object",

                "required": [
                    "title",
                    "content"
                ],

                "properties": {

                    "title": {

                        "type":
                        "string",

                        "example":
                        "Updated Python Notes"
                    },

                    "content": {

                        "type":
                        "string",

                        "example":
                        "Updated note content."
                    }
                }
            }
        }
    ],

    "responses": {

        "200": {

            "description":
            "Note updated successfully"
        },

        "400": {

            "description":
            "Request body or required fields are missing"
        },

        "401": {

            "description":
            "Missing or invalid JWT token"
        },

        "404": {

            "description":
            "Note not found"
        },

        "500": {

            "description":
            "Failed to update note"
        }
    }
})
def update_note(note_id):

    data = request.get_json()

    if not data:

        return jsonify({

            "message":
            "Request body is required"

        }), 400

    user_id = get_jwt_identity()

    note = Note.query.filter_by(

        id=note_id,

        user_id=int(user_id)

    ).first()

    if not note:

        return jsonify({

            "message":
            "Note not found"

        }), 404

    title = data.get("title")

    content = data.get("content")

    if not title or not content:

        return jsonify({

            "message":
            "Title and content are required"

        }), 400

    note.title = title

    note.content = content

    try:

        db.session.commit()

        return jsonify({

            "message":
            "Note updated successfully",

            "note": {

                "id": note.id,

                "user_id": note.user_id,

                "title": note.title,

                "content": note.content,

                "created_at": note.created_at,

                "updated_at": note.updated_at
            }

        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({

            "message":
            "Failed to update note",

            "error": str(e)

        }), 500


# ==================================================
# DELETE NOTE
# DELETE /notes/<note_id>
# ==================================================

@notes_bp.route("/<int:note_id>", methods=["DELETE"])
@jwt_required()
@swag_from({

    "tags": [
        "Notes"
    ],

    "summary": "Delete Note",

    "description": (
        "Delete a note belonging to "
        "the logged-in user."
    ),

    "operationId": "deleteNote",

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
            "note_id",

            "in":
            "path",

            "type":
            "integer",

            "required":
            True,

            "example":
            1
        }
    ],

    "responses": {

        "200": {

            "description":
            "Note deleted successfully"
        },

        "401": {

            "description":
            "Missing or invalid JWT token"
        },

        "404": {

            "description":
            "Note not found"
        },

        "500": {

            "description":
            "Failed to delete note"
        }
    }
})
def delete_note(note_id):

    user_id = get_jwt_identity()

    note = Note.query.filter_by(

        id=note_id,

        user_id=int(user_id)

    ).first()

    if not note:

        return jsonify({

            "message":
            "Note not found"

        }), 404

    try:

        db.session.delete(note)

        db.session.commit()

        return jsonify({

            "message":
            "Note deleted successfully"

        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({

            "message":
            "Failed to delete note",

            "error": str(e)

        }), 500