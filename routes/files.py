from flask import (
    Blueprint,
    request,
    jsonify
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from db import db
from model import Document

from services.document_extractor import (
    extract_text
)

from services.chroma_service import (
    add_document,
    delete_document
)


# ==================================================
# FILE BLUEPRINT
# ==================================================

files_bp = Blueprint(
    "files",
    __name__,
    url_prefix="/files"
)


# ==================================================
# 1. UPLOAD FILE
#
# POST /files/upload
# ==================================================

@files_bp.route(
    "/upload",
    methods=["POST"]
)
@jwt_required()
def upload_file():

    # ----------------------------------------------
    # Get logged-in user ID
    # ----------------------------------------------

    user_id = int(
        get_jwt_identity()
    )

    # ----------------------------------------------
    # Check whether file exists
    # ----------------------------------------------

    if "file" not in request.files:

        return jsonify({

            "message":
                "No file provided"

        }), 400

    file = request.files["file"]

    # ----------------------------------------------
    # Check filename
    # ----------------------------------------------

    if not file.filename:

        return jsonify({

            "message":
                "File name is required"

        }), 400

    try:

        # ------------------------------------------
        # Read file
        # ------------------------------------------

        file_data = file.read()

        if not file_data:

            return jsonify({

                "message":
                    "File is empty"

            }), 400

        # ------------------------------------------
        # File name
        # ------------------------------------------

        file_name = file.filename

        # ------------------------------------------
        # Get extension
        # ------------------------------------------

        file_type = ""

        if "." in file_name:

            file_type = (
                file_name
                .rsplit(".", 1)[1]
                .lower()
            )

        # ------------------------------------------
        # Allow only supported file types
        # ------------------------------------------

        allowed_types = [
            "pdf",
            "docx"
        ]

        if file_type not in allowed_types:

            return jsonify({

                "message":
                    "Unsupported file type",

                "allowed_types":
                    allowed_types

            }), 400

        # ------------------------------------------
        # Create document
        # ------------------------------------------

        document = Document(

            user_id=user_id,

            file_name=file_name,

            file_type=file_type,

            file_data=file_data

        )

        # ------------------------------------------
        # Save to MySQL
        # ------------------------------------------

        db.session.add(
            document
        )

        db.session.commit()

        # ------------------------------------------
        # Response
        # ------------------------------------------

        return jsonify({

            "message":
                "File uploaded successfully",

            "document_id":
                document.id,

            "file_name":
                document.file_name,

            "file_type":
                document.file_type,

            "user_id":
                document.user_id

        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({

            "message":
                "File upload failed",

            "error":
                str(e)

        }), 500


# ==================================================
# 2. GET EXTRACTED TEXT
#
# GET /files/<document_id>/text
# ==================================================

@files_bp.route(
    "/<int:document_id>/text",
    methods=["GET"]
)
@jwt_required()
def get_document_text(
    document_id
):

    # ----------------------------------------------
    # Get logged-in user
    # ----------------------------------------------

    user_id = int(
        get_jwt_identity()
    )

    # ----------------------------------------------
    # Find document belonging to user
    # ----------------------------------------------

    document = Document.query.filter_by(

        id=document_id,

        user_id=user_id

    ).first()

    if not document:

        return jsonify({

            "message":
                "Document not found"

        }), 404

    try:

        # ------------------------------------------
        # Extract text
        # ------------------------------------------

        text = extract_text(

            document.file_data,

            document.file_type

        )

        # ------------------------------------------
        # Check extracted text
        # ------------------------------------------

        if not text:

            return jsonify({

                "message":
                    "No text found in document",

                "document_id":
                    document.id

            }), 400

        # ------------------------------------------
        # Return text
        # ------------------------------------------

        return jsonify({

            "message":
                "Text extracted successfully",

            "document_id":
                document.id,

            "file_name":
                document.file_name,

            "file_type":
                document.file_type,

            "text":
                text

        }), 200

    except Exception as e:

        return jsonify({

            "message":
                "Text extraction failed",

            "error":
                str(e)

        }), 500


# ==================================================
# 3. GET DOCUMENT CHUNKS
#
# GET /files/<document_id>/chunks
# ==================================================

@files_bp.route(
    "/<int:document_id>/chunks",
    methods=["GET"]
)
@jwt_required()
def get_document_chunks(
    document_id
):

    # ----------------------------------------------
    # Get logged-in user
    # ----------------------------------------------

    user_id = int(
        get_jwt_identity()
    )

    # ----------------------------------------------
    # Check document
    # ----------------------------------------------

    document = Document.query.filter_by(

        id=document_id,

        user_id=user_id

    ).first()

    if not document:

        return jsonify({

            "message":
                "Document not found"

        }), 404

    try:

        # ------------------------------------------
        # Extract text
        # ------------------------------------------

        text = extract_text(

            document.file_data,

            document.file_type

        )

        if not text:

            return jsonify({

                "message":
                    "No text found in document"

            }), 400

        # ------------------------------------------
        # Create chunks
        # ------------------------------------------

        from services.chroma_service import (
            create_chunks
        )

        chunks = create_chunks(
            text
        )

        # ------------------------------------------
        # Return chunks
        # ------------------------------------------

        return jsonify({

            "message":
                "Document chunks created successfully",

            "document_id":
                document.id,

            "file_name":
                document.file_name,

            "total_chunks":
                len(chunks),

            "chunks":
                chunks

        }), 200

    except Exception as e:

        return jsonify({

            "message":
                "Chunk creation failed",

            "error":
                str(e)

        }), 500


# ==================================================
# 4. EMBED DOCUMENT
#
# POST /files/<document_id>/embed
# ==================================================

@files_bp.route(
    "/<int:document_id>/embed",
    methods=["POST"]
)
@jwt_required()
def embed_document(
    document_id
):

    # ----------------------------------------------
    # Get logged-in user
    # ----------------------------------------------

    user_id = int(
        get_jwt_identity()
    )

    # ----------------------------------------------
    # Find document
    # ----------------------------------------------

    document = Document.query.filter_by(

        id=document_id,

        user_id=user_id

    ).first()

    if not document:

        return jsonify({

            "message":
                "Document not found"

        }), 404

    try:

        # ------------------------------------------
        # Extract text
        # ------------------------------------------

        text = extract_text(

            document.file_data,

            document.file_type

        )

        if not text:

            return jsonify({

                "message":
                    "No text found in document"

            }), 400

        # ------------------------------------------
        # Send text to ChromaDB
        # ------------------------------------------

        result = add_document(

            document_id=document.id,

            user_id=user_id,

            file_name=document.file_name,

            text=text

        )

        # ------------------------------------------
        # Return result
        # ------------------------------------------

        return jsonify({

            "message":
                "Document embedded successfully",

            "document_id":
                document.id,

            "file_name":
                document.file_name,

            "chunks_stored":
                result.get(
                    "chunks_stored",
                    0
                )

        }), 200

    except Exception as e:

        return jsonify({

            "message":
                "Document embedding failed",

            "error":
                str(e)

        }), 500


# ==================================================
# 5. DELETE CHROMADB EMBEDDINGS
#
# DELETE /files/<document_id>/vector
# ==================================================

@files_bp.route(
    "/<int:document_id>/vector",
    methods=["DELETE"]
)
@jwt_required()
def delete_document_vector(
    document_id
):

    # ----------------------------------------------
    # Get logged-in user
    # ----------------------------------------------

    user_id = int(
        get_jwt_identity()
    )

    # ----------------------------------------------
    # Find document
    # ----------------------------------------------

    document = Document.query.filter_by(

        id=document_id,

        user_id=user_id

    ).first()

    if not document:

        return jsonify({

            "message":
                "Document not found"

        }), 404

    try:

        # ------------------------------------------
        # Delete vectors from ChromaDB
        # ------------------------------------------

        delete_document(
            document_id
        )

        return jsonify({

            "message":
                "Document embeddings deleted successfully",

            "document_id":
                document.id

        }), 200

    except Exception as e:

        return jsonify({

            "message":
                "Failed to delete embeddings",

            "error":
                str(e)

        }), 500