#!/usr/bin/env python3
"""Basic Auth module
"""
import re
from typing import TypeVar
from api.v1.auth.auth import Auth
import base64

class BasicAuth(Auth):
    """BasicAuthentication class"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        : to handle and return the Base64 part of the Authorization header
        for basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]
    

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        : to return the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.base64decode(base64_authorization_header)
        except base64.binascii.Error:
            return None
        
        return decoded_bytes.decode('utf-8')