import io
import os

from PIL import Image
from google import genai
from google.genai import types


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY is missing from .env")

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# IMAGE TEXT EXTRACTION USING GEMINI
# ============================================================

def extract_text_from_image(file_data, file_type):
    """
    Extract text/content from an uploaded image using Gemini.

    Supported image types:
    jpg, jpeg, png, gif, webp, bmp, tiff
    """

    try:
        # ----------------------------------------------------
        # Check that the uploaded file is a valid image
        # ----------------------------------------------------

        image = Image.open(io.BytesIO(file_data))
        image.verify()

        # ----------------------------------------------------
        # MIME TYPE
        # ----------------------------------------------------

        mime_types = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "webp": "image/webp",
            "bmp": "image/bmp",
            "tiff": "image/tiff"
        }

        mime_type = mime_types.get(file_type.lower())

        if not mime_type:
            raise Exception(
                f"Unsupported image type: {file_type}"
            )

        # ----------------------------------------------------
        # GEMINI PROMPT
        # ----------------------------------------------------

        prompt = """
Extract all meaningful readable text from this image.

Rules:

1. Extract the text accurately.
2. Preserve the original wording as much as possible.
3. Include headings, labels, numbers and important text.
4. If there is a table, preserve its information in a readable
   text format.
5. If there is handwritten text and it is readable, extract it.
6. Do not describe the image.
7. Do not explain anything.
8. Return only the extracted text.
9. If there is no readable text, return an empty response.
"""

        # ----------------------------------------------------
        # SEND IMAGE + PROMPT TO GEMINI
        # ----------------------------------------------------

        image_part = types.Part.from_bytes(
            data=file_data,
            mime_type=mime_type
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                image_part,
                prompt
            ]
        )

        # ----------------------------------------------------
        # RETURN EXTRACTED TEXT
        # ----------------------------------------------------

        if not response:
            return ""

        if not response.text:
            return ""

        return response.text.strip()

    except Exception as e:
        raise Exception(
            f"Image text extraction failed: {str(e)}"
        )


# ============================================================
# GENERAL TEXT EXTRACTION
# ============================================================

def extract_text(file_data, file_type):
    """
    Extract text from uploaded files.

    Supported:
        - JPG
        - JPEG
        - PNG
        - GIF
        - WEBP
        - BMP
        - TIFF
        - PDF
        - DOCX

    DOC is currently not supported.
    """

    file_type = file_type.lower()

    # ========================================================
    # IMAGE FILES
    # ========================================================

    image_types = [
        "jpg",
        "jpeg",
        "png",
        "gif",
        "webp",
        "bmp",
        "tiff"
    ]

    if file_type in image_types:

        return extract_text_from_image(
            file_data,
            file_type
        )

    # ========================================================
    # PDF
    # ========================================================

    if file_type == "pdf":

        from PyPDF2 import PdfReader

        pdf_file = io.BytesIO(file_data)

        reader = PdfReader(pdf_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    # ========================================================
    # DOCX
    # ========================================================

    if file_type == "docx":

        from docx import Document

        doc_file = io.BytesIO(file_data)

        document = Document(doc_file)

        text = ""

        for paragraph in document.paragraphs:

            if paragraph.text:
                text += paragraph.text + "\n"

        return text.strip()

    # ========================================================
    # DOC
    # ========================================================

    if file_type == "doc":

        raise Exception(
            "DOC format text extraction is not currently configured"
        )

    # ========================================================
    # UNSUPPORTED FILE TYPE
    # ========================================================

    raise Exception(
        f"Unsupported file type: {file_type}"
    )
