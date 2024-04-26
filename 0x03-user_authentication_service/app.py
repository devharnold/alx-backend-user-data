#!/usr/bin/env python3
from flask import Flask
from flask import jsonify, request, abort, redirect
from auth import Auth
app = Flask(__name__)
AUTH = Auth()

@app.route("/", methods=['GET'])
def welcome():
    """returns a jsonified welcome message
    """
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"])
def register_user(email: str, password: str) -> str:
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
def login() -> str:
    """The request is expected to contain form data with email and password fields
    If the login information is incorrect, use flask.abort to respond with a 401 HTTP status
    Otherwise create a new session or the user, store the sessionID
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """The request is expected to contain the session ID as a cookie with key "session_id".
    Find the user with the requested session ID. If the user exists destroy the session and redirect
    the user to GET /. If the user does not exist, respond with a 403 HTTP status.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")
    
@app.route("/profile", methods=["GET"])
def get_profile() -> str:
    """
    Get a profile route
    The request is expected to contain a session_id cookie
    if user exists respond with status 200 and a JSON payload <{"email": "<user email>"}>.
    If the user does not exist, respond with a 403 HTTP status
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})

@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """
    The request is expected to contain form data with the "email" field
    If email is not registered, respond with 403 satus code
    Otherwise generate a token and a HTTP response
    """
    email = request.form.get('email')
    reset_token = None
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        reset_token = None
    if reset_token is None:
        abort(403)
    return jsonify({"email": email, "reset_token": token})
    
@app.route("/reset_password", methods=["PUT"])
def update_password():
    """Update password with "email", "reset_token", and "new_password" fields
    If token is invalid, catch the exception and respond with a 403 HTTP code.
    If the token is valid, respond with a 200 status code
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    is_password_change = False
    try:
        AUTH.update_password(reset_token, new_password)
        is_password_change = True
    except ValueError:
        is_password_change = False
    if not is_password_change:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")