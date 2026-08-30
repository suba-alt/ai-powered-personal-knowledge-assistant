from db import db


# =========================
# USER MODEL
# =========================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )


# =========================
# NOTES MODEL
# =========================

class Note(db.Model):

    __tablename__ = "scan_notes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    title = db.Column(
        db.String(255),
        nullable=True
    )

    content = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    updated_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )


# =========================
# DOCUMENT MODEL
# =========================

class Document(db.Model):

    __tablename__ = "documents"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    file_name = db.Column(
        db.String(255),
        nullable=True
    )

    file_type = db.Column(
        db.String(50),
        nullable=True
    )

    file_data = db.Column(
        db.LargeBinary,
        nullable=True
    )

    uploaded_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=db.func.current_timestamp()
    )