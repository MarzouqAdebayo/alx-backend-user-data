#!/usr/bin/env python3
"""Module 'session_auth.py' """
import os
from typing import Tuple
from flask import request, jsonify, abort
from api.v1.views import app_views


@app_views.route(
    "/auth_session/login",
    methods=["POST"],
    strict_slashes=False,
)
def login() -> Tuple[str, int]:
    """POST /api/v1/auth_session/login
    Return:
        - JSON representation of a User object
    """
    user_email = request.form.get("email")
    if not user_email or not len(user_email.strip()):
        return jsonify({"error": "email missing"}), 400
    user_pwd = request.form.get("password")
    if not user_pwd or not len(user_pwd.strip()):
        return jsonify({"error": "password missing"}), 400
    from models.user import User

    users = User.search({"email": user_email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not users[0].is_valid_password(user_pwd):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth

    session_id = auth.create_session(getattr(users[0], "id"))
    response = jsonify(users[0].to_json())
    session_name = os.getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)
    return response


@app_views.route(
    "/auth_session/logout",
    methods=["DELETE"],
    strict_slashes=False,
)
def logout() -> Tuple[str, int]:
    """GET /api/v1/auth_session/logout"""
    from api.v1.app import auth

    destroyed = auth.destroy_session(request)
    if not destroyed:
        abort(404)
    return jsonify({}), 200
