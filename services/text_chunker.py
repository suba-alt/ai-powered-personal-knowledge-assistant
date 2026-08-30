# services/text_chunker.py


# =========================
# CLEAN TEXT
# =========================

def clean_text(text):
    """
    Clean unnecessary whitespace from extracted text.
    """

    if not text:
        return ""

    # Split into lines
    lines = text.splitlines()

    # Remove unnecessary spaces
    cleaned_lines = []

    for line in lines:

        line = line.strip()

        if line:
            cleaned_lines.append(line)

    # Join lines
    cleaned_text = " ".join(cleaned_lines)

    # Remove repeated spaces
    cleaned_text = " ".join(
        cleaned_text.split()
    )

    return cleaned_text


# =========================
# SPLIT TEXT INTO CHUNKS
# =========================

def chunk_text(
    text,
    chunk_size=1000,
    overlap=200
):
    """
    Split text into overlapping chunks.

    chunk_size:
        Maximum number of characters in a chunk.

    overlap:
        Number of characters repeated between
        consecutive chunks.
    """

    # Clean the text first
    text = clean_text(text)

    if not text:
        return []

    # Validate values
    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if overlap < 0:
        raise ValueError(
            "overlap cannot be negative"
        )

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    chunks = []

    start = 0

    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end]

        # Remove unnecessary whitespace
        chunk = chunk.strip()

        if chunk:
            chunks.append(chunk)

        # Move forward while keeping overlap
        start = end - overlap

    return chunks