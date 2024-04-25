#!/usr/bin/env python3
from flask import Flask
from flask import jsonify, request
from auth import Auth
app = Flask(__name__)
AUTH = Auth()

@app.route("/", methods=['GET'])
def welcome():
    """returns a jsonified welcome message
    """
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"])
def register_user(email: str, password: str):
    """implements the POST /users route
    the endpoint shoud expect two form data fields; email and password
    if the user does not exist, the endpoint should register it and respond 
    with a JSON payload <{"email": "<registered email>", "message": "user created"}>
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route("/sessions", methods=["POST"])
def login():
    """The request is expected to contain form data with email and password fields
    If the login information is incorrect, use flask.abort to respond with a 401 HTTP status
    Otherwise create a new session or the user, store the sessionID
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        return jsonify({"email": email, "message": "logged in"})
    else:
        return jsonify({"message": "wrong password"}), 401

@app.route("/sessions", methods=["DELETE"])
def logout():
    """The request is expected to contain the session ID as a cookie with key "session_id".
    Find the user with the requested session ID. If the user exists destroy the session and redirect
    the user to GET /. If the user does not exist, respond with a 403 HTTP status.
    """
    session_id = request.cookies.get('session_id')
    if AUTH.destroy_session(session_id):
        return jsonify({"message": "Bienvenue"})
    else:
        return jsonify({"message": "Unauthorized"}), 403
    
@app.route("/profile", methods=["GET"])
def get_profile():
    """
    Get a profile route
    The request is expected to contain a session_id cookie
    if user exists respond with status 200 and a JSON payload <{"email": "<user email>"}>.
    If the user does not exist, respond with a 403 HTTP status
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    else:
        return jsonify({"message": "Unauthorized"}), 403
    
@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """
    The request is expected to contain form data with the "email" field
    If email is not registered, respond with 403 satus code
    Otherwise generate a token and a HTTP response
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        return jsonify({"message": "Unauthorized"}), 403
    
@app.route("/reset_password", methods=["PUT"])
def update_password():
    """Update password with "email", "reset_token", and "new_password" fields
    If token is invalid, catch the exception and respond with a 403 HTTP code.
    If the token is valid, respond with a 200 status code
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(email, reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        return jsonify({"message": "Unauthorized"}), 403   

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")