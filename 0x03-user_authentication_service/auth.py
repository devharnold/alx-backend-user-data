#!/usr/bin/env python3
import bcrypt
from sqlalchemy import Column, Integer, String
from db import DB
from user import User, Base
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth
from uuid import uuid
from user import User, Base

def _hash_password(password: str) -> bytes:
    """
    takes in a password string and returns bytes
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

class Auth:
    """
    Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()

    @property
    def _db(self):
        return self._db
    
    def register_user(self, email: str, password: str)-> User:
        """
        takes in mandatory args as email and password
        if user already exists with the passed email and password
        raise a ValueError with message: user already exists
        If not, hash the password with _hash_password, save the user to the db
        """
        try:
            Auth._db.find_user(email)
            raise ValueError(f"User's {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        
    def valid_login(self, email: str, password: str) -> bool:
        """try locating user by email.
        if exists, check the password with bcrypt.checkpw
        if it matches return True, otherwise; False
        """
        user = Auth.valid_login(email, password)
        if user:
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        else:
            return False
        
    def _generate_uuid() -> str[uuid]:
        """generates a random uuid 
        and returns the string representation of a new UUID
        """
        return uuid()
    
    def create_session(self, email: str) -> str:
        """
        Takes in email and returns the sessionId as string
        This method is meant to find the user corresponding to the email, generate a new UUID and 
        store it in the database s the user's session ID
        """
        user = self.db.find_user_by(email)
        if user:
            session_id = str(uuid.uuid4())
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        else:
            return None
        

    def get_user_from_session_id(session_id: str) -> None:
        """if session id is None, or no user found, return None
        Otherwise return corresponding user
        """
        if session_id is None:
            return None
        user = Auth._db.find_user_by(session_id=session_id)
        if user:
            return user
        else:
            return None
        
    def destroy_session(self, user_id: int) -> None:
        """
        destroy a session after taking
        : parameter; user_id(int) 
        The method updates the user's session ID to None
        """
        user = self._db.find_user_by(user_id)
        if user:
            Auth.destroy_session(user_id)
        else:
            return None