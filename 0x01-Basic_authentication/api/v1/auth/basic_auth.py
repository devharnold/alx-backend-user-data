#!/usr/bin/env python3
"""Basic Auth module
"""
import re
from typing import TypeVar
from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """BasicAuthentication class"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Function to handle and return the Base64 part of the Authorization header
        for basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]