#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import Optional

from user import Base, User

class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def add_user(email: str, hashed_password: str):
        """Add a user with email and hashed_password as the arguments
        : params; email(str) The email address of the user
                  hashed_password(str) The password of the user
        Returns a new user object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        session.add(new_user)
        session.commit()
        return new_user
    
    def find_user(user_id: int)-> Optional[User]:
        """
        Find user by their email address from the db
        Parameters:
            email(str): The user's email address
        Returns:
            User: The user object if found,or None if not found
        """
        return session.query(User).filter_by(email=user_id).first()
    
    def update_user(user_id: int, **kwargs) -> None:
        """Updates a user by the user_id instance.
        Parameters:
            user_id(int): The unique identifier of the various users
        Returns:
            None"""
        user = DB.find_user_by(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid attribute '{key}' for user.")
            session.commit()
        else:
            print("User not found.")

    