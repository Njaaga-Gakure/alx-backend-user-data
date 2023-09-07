#!/usr/bin/env python3
"""Module for session auth routes."""


from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handle login."""
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user_list = User.search({"email": email})
    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404
    for user in user_list:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        session_name = getenv("SESSION_NAME")
        response = jsonify(user.to_json())
        response.set_cookie(session_name, session_id)
        return response