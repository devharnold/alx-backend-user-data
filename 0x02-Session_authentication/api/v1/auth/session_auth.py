#!/usr/bin/env python3
"""session auth module
"""
import os
from api.v1.auth.auth import Auth

class SessionAuth(Auth):
    """SessionAuthenticate class
    """
    pass

    def validate_inheritance():
        """
        : to check if sessionauth inherits from auth
        """
        if issubclass(SessionAuth, Auth):
            print('SessionAuth inherits successfully from Auth')
        else:
            print("SessionAuth does not inherit!")

    def validate_switch():
        """
        : to check environment variable to determine authentication mechanism
        """
        auth_mechanism = os.environ.get("AUTH_MECHANISM")

        if auth_mechanism == "session":
            print("Using SessionAuth for authentication")
            auth = SessionAuth()
        else:
            print("Using Auth for authentication")
            auth = Auth()