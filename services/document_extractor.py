from io import BytesIO

from PyPDF2 import PdfReader
from docx import Document as DocxDocument


# ==================================================
# EXTRACT TEXT FROM PDF
# ==================================================

def extract_pdf_text(file_data):

    pdf_file = BytesIO(file_data)

    reader = PdfReader(pdf_file)

    text_parts = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text_parts.append(page_text)

    return "\n".join(text_parts).strip()


# ==================================================
# EXTRACT TEXT FROM DOCX
# ==================================================

def extract_docx_text(file_data):

    docx_file = BytesIO(file_data)

    document = DocxDocument(docx_file)

    text_parts = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:

            text_parts.append(text)

    return "\n".join(text_parts).strip()


# ==================================================
# EXTRACT TEXT FROM TXT
# ==================================================

def extract_txt_text(file_data):

    return file_data.decode(
        "utf-8",
        errors="ignore"
    ).strip()


# ==================================================
# GENERAL TEXT EXTRACTION
# ==================================================

def extract_text(
    file_data,
    file_type
):

    if not file_data:

        raise ValueError(
            "File data is empty"
        )

    file_type = (
        file_type
        .lower()
        .replace(".", "")
        .strip()
    )

    # ------------------------------------------
    # PDF
    # ------------------------------------------

    if file_type == "pdf":

        return extract_pdf_text(
            file_data
        )

    # ------------------------------------------
    # DOCX
    # ------------------------------------------

    elif file_type == "docx":

        return extract_docx_text(
            file_data
        )

    # ------------------------------------------
    # TXT
    # ------------------------------------------

    elif file_type == "txt":

        return extract_txt_text(
            file_data
        )

    # ------------------------------------------
    # Unsupported file
    # ------------------------------------------

    else:

        raise ValueError(
            f"Unsupported file type: {file_type}"
        )