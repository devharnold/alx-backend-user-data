#!/usr/bin/python3
"""Password Encryption module.
"""
import bcrypt

def hash_password(password: str) -> bytes:
    """Hashes a password we will use salt
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def is_valid(hashed_password: bytes, password: str) -> bool:
    """check if the hashed pw originates from the given password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)