#!/usr/bin/env python3
"""Basic Auth module
"""
import re
from typing import TypeVar, Tuple
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
        if (base64_authorization_header) == str:
            try:
                result = base64.base64deocde(base64_authorization_header, validate=True)
                return result.decode('utf-8')
            except (base64.binascii.Error, UnicodeDecodeError):
                return None

        #if base64_authorization_header is None:
        #    return None
        #if not isinstance(base64_authorization_header, str):
        #    return None
        #try:
        #    decoded_bytes = base64.base64decode(base64_authorization_header)
        #except base64.binascii.Error:
        #    return None
        #
        #return decoded_bytes.decode('utf-8')
    
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        : function used to return the user email and password from the Base64 decoded value
        """
        if type(decoded_base64_authorization_header) == str:
            pattern = r'user:password'
            field_match = re.fullmatch(pattern, decoded_base64_authorization_header.strip())
            if field_match is not None:
                user = field_match.group('user')
                password = field_match.group('password')
                return user, password
        return None, None

        #if decoded_base64_authorization_header is None:
        #    return None
        #if not isinstance(decoded_base64_authorization_header, str):
        #    return None
        #
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        : returns the `user` instance based on his email and password
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({"email": user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
        : retrieves the user from a request
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)