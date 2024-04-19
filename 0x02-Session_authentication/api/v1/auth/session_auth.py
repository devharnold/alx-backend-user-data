#!/usr/bin/env python3
"""session auth module
"""
import os
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User
from flask import request
class SessionAuth(Auth):
    """SessionAuthenticate class
    """
    user_id_by_session_id = {}
    
    def create_session(self, user_id: str = None) -> str:
        """
        : creates a SessionId for `user_id`
        """
        if type(user_id)is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        : returns a userID based on a SessionID
        Args:
            session_id(str): the session id
        Return:
            A string user ID associated with the sessionID
        """
        if type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)
        
    def current_user(self, request=None):
        """
        : returns a user instance based on a cookie value
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)
    
    def destroy_session(self, request=None):
        """
        : to destroy an authenticated session
        Args:
            request(object): the request object
        Return: True if the session was successfuly destroyed
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True