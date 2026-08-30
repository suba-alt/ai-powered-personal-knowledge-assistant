from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from db import db
from model import Note


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
            "message": "Title and content are required"
        }), 400

    # Get logged-in user's ID from JWT
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
            "message": "Note created successfully",
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
            "message": "Failed to create note",
            "error": str(e)
        }), 500


# ==================================================
# VIEW ALL NOTES
# GET /notes
# ==================================================

@notes_bp.route("", methods=["GET"])
@jwt_required()
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
        "message": "Notes retrieved successfully",
        "notes": notes_list
    }), 200


# ==================================================
# VIEW ONE NOTE
# GET /notes/<id>
# ==================================================

@notes_bp.route("/<int:note_id>", methods=["GET"])
@jwt_required()
def get_note(note_id):

    user_id = get_jwt_identity()

    note = Note.query.filter_by(
        id=note_id,
        user_id=int(user_id)
    ).first()

    if not note:

        return jsonify({
            "message": "Note not found"
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
# PUT /notes/<id>
# ==================================================

@notes_bp.route("/<int:note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "Request body is required"
        }), 400

    user_id = get_jwt_identity()

    note = Note.query.filter_by(
        id=note_id,
        user_id=int(user_id)
    ).first()

    if not note:

        return jsonify({
            "message": "Note not found"
        }), 404

    title = data.get("title")
    content = data.get("content")

    if not title or not content:

        return jsonify({
            "message": "Title and content are required"
        }), 400

    note.title = title
    note.content = content

    try:

        db.session.commit()

        return jsonify({
            "message": "Note updated successfully",
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
            "message": "Failed to update note",
            "error": str(e)
        }), 500


# ==================================================
# DELETE NOTE
# DELETE /notes/<id>
# ==================================================

@notes_bp.route("/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):

    user_id = get_jwt_identity()

    note = Note.query.filter_by(
        id=note_id,
        user_id=int(user_id)
    ).first()

    if not note:

        return jsonify({
            "message": "Note not found"
        }), 404

    try:

        db.session.delete(note)
        db.session.commit()

        return jsonify({
            "message": "Note deleted successfully"
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "message": "Failed to delete note",
            "error": str(e)
        }), 500