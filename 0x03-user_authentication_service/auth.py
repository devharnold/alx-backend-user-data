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

def _generate_uuid() -> str:
    """Generates a uuid
    Return: A string representation of the uuid
    """
    return str(uuid())

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
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User's {email} already exists")
        
    def valid_login(self, email: str, password: str) -> bool:
        """try locating user by email.
        if exists, check the password with bcrypt.checkpw
        if it matches return True, otherwise; False
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False
        return False
    
    def create_session(self, email: str) -> str:
        """
        Takes in email and returns the sessionId as string
        This method is meant to find the user corresponding to the email, generate a new UUID and 
        store it in the database s the user's session ID
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
    

    def get_user_from_session_id(self, session_id: str) -> None:
        """if session id is None, or no user found, return None
        Otherwise return corresponding user
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return None
        
    def destroy_session(self, user_id: int) -> None:
        """
        destroy a session after taking
        : parameter; user_id(int) 
        The method updates the user's session ID to None
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password(self, email: str) -> str:
        """Gets a password reset token for the user
        Paramaters:
            email: The address of the user
        Returns:
            The generated password reset token
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

