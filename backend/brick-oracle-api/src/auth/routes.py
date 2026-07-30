"""Auth endpoints: register and login.

The user's id is stored client-side and echoed back for identification only.
"""

from __future__ import annotations

import uuid

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db
from ..models.catalog import User
from ..catalog.repository import get_user_by_email, get_user_by_username

auth_bp = Blueprint("auth", __name__)


def _user_to_dict(user: User) -> dict[str, str]:
    return {"id": user.id, "username": user.username, "email": user.email}


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not email or not username or not password:
        return jsonify({"error": "Email, username, and password are required."}), 400

    if get_user_by_email(email) is not None:
        return jsonify({"error": "Email is already registered."}), 409

    if get_user_by_username(username) is not None:
        return jsonify({"error": "Username is already taken."}), 409

    user = User(
        id=uuid.uuid4().hex,
        username=username,
        email=email,
        name=username,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"token": user.id, "user": _user_to_dict(user)}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = get_user_by_email(email)
    if user is None or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password."}), 401

    return jsonify({"token": user.id, "user": _user_to_dict(user)}), 200
