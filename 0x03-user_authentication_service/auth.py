#!/usr/bin/env python3
import bcrypt
from sqlalchemy import Column, Integer, String
from db import DB
from user import User, Base
from sqlalchemy.orm.exc import NoResultFound

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
            self._db.find_user(email)
            raise ValueError(f"User's {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
            