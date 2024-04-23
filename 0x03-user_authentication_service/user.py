#!/usr/bin/env python3
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """create a class user which inherits from base"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

    def __repr__(self):
        """return a formal string representation"""
        return f"<User(id={self.id}, email={self.email}, hashed_password={self.hashed_password},\
            session_id={self.session_id}, reset_token={self.reset_token})>"


