#!/usr/bin/env python3
import bcrypt
from sqlalchemy import Column, Integer, String


def _hash_password(password: str) -> bytes:
    """
    takes in a password string and returns bytes
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())