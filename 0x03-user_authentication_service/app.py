#!/usr/bin/env python3
"""Flask application."""


from flask import (Flask,
                   jsonify,
                   request,
                   abort,
                   make_response)
from auth import Auth


AUTH = Auth()


app = Flask(__name__)


@app.route('/')
def index():
    """Index route."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Register a user."""
    email = request.form['email']
    password = request.form['password']
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Handle login."""
    email = request.form.get('email')
    password = request.form.get('password')
    is_valid = AUTH.valid_login(email, password)
    if not is_valid:
        abort(401)
    session_id = AUTH.create_session(email)
    if session_id:
        response = make_response({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")