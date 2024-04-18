#!/usr/bin/env python3
"""auth module
"""
from flask import Flask
from flask import request
from typing import List, TypeVar
import re
import os


class Auth:
    """auth base class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check for need of authentication in a path"""
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True
    
    def authorization_header(self, request=None) -> str:
        """flask request object to handle the authorization header
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """handles the current user"""
        return None
    
    def session_cookies(self, request=None):
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)