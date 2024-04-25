#!/usr/bin/env python3
from flask import Flask
from flask import jsonify
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

@app.route("/", methods=['GET'])
def welcome():
    """returns a jsonified welcome message
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
