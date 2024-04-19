#!/usr/bin/env python3
"""
views-auth module
"""
import os
from flask import abort, jsonify, request
from typing import Tuple

from models.user import User
from api.v1.views import app_views

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """
    : this is responsible for handling user login using session auth
    User provides their email and password, such that if they are correct, it validates, if not it 
    renders an error and the function does not proceed
    """
    not_found_response = {"error": "no user found for this email"}
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "internal server error"}), 500
    
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    
    return jsonify(user.serialize()), 200
    