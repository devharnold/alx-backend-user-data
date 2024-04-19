#!/usr/bin/env python3
"""
SessionExpAuth Module
"""
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime

class SessionExpAuth(SessionAuth):
    """class SessionAuth with Expiration date"""
    def __init__(self, session_duration):
        """: class initialization with an overload"""
        self.session_duration = session_duration

        session_duration_str = os.environ.get("SESSION_DURATION")
        try:
            session_duration = int(session_duration_str) if session_duration_str else 0
        except (TypeError, ValueError):
            self.session_duration = 0
    
    def create_session(self, user_id=None):
        """
        : creates a sessionID
        Value of the key[user_id_by_session_id] must be a dictionary called(session dictionary)
        Args:
            super(): when called, it will call the `create_session()` method of the SessionAuth
        Return: None if `super()` cant create a SessionID
        """
        super().create_session()
        try:
            super().create_session()
        except Exception as e:
            return None
        

        #session_id = super().create_session()
        #try:
        #    super().create_session()
        #except Exception as e:
        #    return None
        #
        #if session_id is None:
        #    return None
        #
        #if type(user_id) is str:
        #    session_id = str(uuid4())
        
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.datetime.now()
        }
        user_id_by_session_id[session_id] = session_dict

        return session_id
    
    def user_id_for_session_id(self, session_id=None):
        """
        : to destroy a session
        Args:
            request(object) -> the request object
        Return: `True` if the session was successfully destroyed
        """
        session_id = self.session