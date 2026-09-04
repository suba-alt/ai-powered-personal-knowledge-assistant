from flask import (
    Blueprint,
    request,
    jsonify
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from flasgger import swag_from

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
# SUPPORTED FILE TYPES
# ==================================================

ALLOWED_FILE_TYPES = [

    "pdf",
    "doc",
    "docx",

    "jpg",
    "jpeg",
    "png",
    "gif",
    "webp",
    "bmp",
    "tiff"

]


# ==================================================
# IMAGE FILE TYPES
# ==================================================

IMAGE_FILE_TYPES = [

    "jpg",
    "jpeg",
    "png",
    "gif",
    "webp",
    "bmp",
    "tiff"

]


# ==================================================
# 1. UPLOAD FILE
# POST /files/upload
# ==================================================

@files_bp.route(
    "/upload",
    methods=["POST"]
)
@jwt_required()
@swag_from({

    "tags": [
        "Files"
    ],

    "summary": "Upload File",

    "description": (
        "Upload a PDF, DOC, DOCX, "
        "or image file."
    ),

    "operationId": "uploadFile",

    "consumes": [
        "multipart/form-data"
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
            "name": "file",

            "in": "formData",

            "type": "file",

            "required": True,

            "description": (
                "Select a PDF, DOC, DOCX, JPG, JPEG, "
                "PNG, GIF, WEBP, BMP, or TIFF file."
            )
        }

    ],

    "responses": {

        "201": {

            "description":
                "File uploaded successfully",

            "examples": {

                "application/json": {

                    "message":
                        "File uploaded successfully",

                    "document_id": 1,

                    "file_name":
                        "python_notes.pdf",

                    "file_type":
                        "pdf",

                    "file_category":
                        "pdf",

                    "user_id": 1
                }
            }
        },

        "400": {

            "description":
                "No file, empty file, or unsupported file type"
        },

        "401": {

            "description":
                "Missing or invalid JWT token"
        },

        "500": {

            "description":
                "File upload failed"
        }
    }

})
def upload_file():

    # ----------------------------------------------
    # Get logged-in user ID
    # ----------------------------------------------

    user_id = int(
        get_jwt_identity()
    )

    # ----------------------------------------------
    # Check file
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
        # File extension
        # ------------------------------------------

        file_type = ""

        if "." in file_name:

            file_type = (
                file_name
                .rsplit(".", 1)[1]
                .lower()
            )

        # ------------------------------------------
        # Validate file type
        # ------------------------------------------

        if file_type not in ALLOWED_FILE_TYPES:

            return jsonify({

                "message":
                    "Unsupported file type",

                "file_type":
                    file_type,

                "allowed_types":
                    ALLOWED_FILE_TYPES

            }), 400

        # ------------------------------------------
        # Detect category
        # ------------------------------------------

        if file_type in IMAGE_FILE_TYPES:

            file_category = "image"

        elif file_type == "pdf":

            file_category = "pdf"

        elif file_type in ["doc", "docx"]:

            file_category = "document"

        else:

            file_category = "unknown"

        # ------------------------------------------
        # Create Document
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

        db.session.add(document)

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

            "file_category":
                file_category,

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
# GET /files/<document_id>/text
# ==================================================

@files_bp.route(
    "/<int:document_id>/text",
    methods=["GET"]
)
@jwt_required()
@swag_from({

    "tags": [
        "Files"
    ],

    "summary": "Get Extracted Text",

    "description": (
        "Extract text/content from the uploaded file."
    ),

    "operationId": "getDocumentText",

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
            "name": "document_id",

            "in": "path",

            "type": "integer",

            "required": True,

            "example": 1
        }

    ],

    "responses": {

        "200": {
            "description":
                "Text extracted successfully"
        },

        "400": {
            "description":
                "No text found in file"
        },

        "401": {
            "description":
                "Missing or invalid JWT token"
        },

        "404": {
            "description":
                "Document not found"
        },

        "500": {
            "description":
                "Text extraction failed"
        }
    }

})
def get_document_text(document_id):

    user_id = int(
        get_jwt_identity()
    )

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

        text = extract_text(

            document.file_data,

            document.file_type

        )

        if not text:

            return jsonify({

                "message":
                    "No text found in file",

                "document_id":
                    document.id,

                "file_type":
                    document.file_type

            }), 400

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
# GET /files/<document_id>/chunks
# ==================================================

@files_bp.route(
    "/<int:document_id>/chunks",
    methods=["GET"]
)
@jwt_required()
@swag_from({

    "tags": [
        "Files"
    ],

    "summary": "Get Document Chunks",

    "description": (
        "Extract text and split the document "
        "into chunks."
    ),

    "operationId": "getDocumentChunks",

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
            "name": "document_id",

            "in": "path",

            "type": "integer",

            "required": True,

            "example": 1
        }

    ],

    "responses": {

        "200": {
            "description":
                "Document chunks created successfully"
        },

        "400": {
            "description":
                "No text found in file"
        },

        "401": {
            "description":
                "Missing or invalid JWT token"
        },

        "404": {
            "description":
                "Document not found"
        },

        "500": {
            "description":
                "Chunk creation failed"
        }
    }

})
def get_document_chunks(document_id):

    user_id = int(
        get_jwt_identity()
    )

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

        text = extract_text(

            document.file_data,

            document.file_type

        )

        if not text:

            return jsonify({

                "message":
                    "No text found in file"

            }), 400

        from services.chroma_service import (
            create_chunks
        )

        chunks = create_chunks(text)

        return jsonify({

            "message":
                "Document chunks created successfully",

            "document_id":
                document.id,

            "file_name":
                document.file_name,

            "file_type":
                document.file_type,

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
# POST /files/<document_id>/embed
# ==================================================

@files_bp.route(
    "/<int:document_id>/embed",
    methods=["POST"]
)
@jwt_required()
@swag_from({

    "tags": [
        "Files"
    ],

    "summary": "Embed Document",

    "description": (
        "Extract the document text, create chunks, "
        "and store embeddings in ChromaDB."
    ),

    "operationId": "embedDocument",

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
            "name": "document_id",

            "in": "path",

            "type": "integer",

            "required": True,

            "example": 1
        }

    ],

    "responses": {

        "200": {
            "description":
                "Document embedded successfully"
        },

        "400": {
            "description":
                "No text found in file"
        },

        "401": {
            "description":
                "Missing or invalid JWT token"
        },

        "404": {
            "description":
                "Document not found"
        },

        "500": {
            "description":
                "Document embedding failed"
        }
    }

})
def embed_document(document_id):

    user_id = int(
        get_jwt_identity()
    )

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

        text = extract_text(

            document.file_data,

            document.file_type

        )

        if not text:

            return jsonify({

                "message":
                    "No text found in file"

            }), 400

        result = add_document(

            document_id=document.id,

            user_id=user_id,

            file_name=document.file_name,

            text=text

        )

        return jsonify({

            "message":
                "Document embedded successfully",

            "document_id":
                document.id,

            "file_name":
                document.file_name,

            "file_type":
                document.file_type,

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
# DELETE /files/<document_id>/vector
# ==================================================

@files_bp.route(
    "/<int:document_id>/vector",
    methods=["DELETE"]
)
@jwt_required()
@swag_from({

    "tags": [
        "Files"
    ],

    "summary": "Delete Document Embeddings",

    "description": (
        "Delete the document embeddings "
        "from ChromaDB."
    ),

    "operationId": "deleteDocumentVector",

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
            "name": "document_id",

            "in": "path",

            "type": "integer",

            "required": True,

            "example": 1
        }

    ],

    "responses": {

        "200": {
            "description":
                "Document embeddings deleted successfully"
        },

        "401": {
            "description":
                "Missing or invalid JWT token"
        },

        "404": {
            "description":
                "Document not found"
        },

        "500": {
            "description":
                "Failed to delete embeddings"
        }
    }

})
def delete_document_vector(document_id):

    user_id = int(
        get_jwt_identity()
    )

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