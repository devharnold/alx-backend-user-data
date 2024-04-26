#!/usr/bin/env python3
"""DB module.

This module contains the DB class, which provides methods for interacting with the database.
"""

from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class.

    This class represents the database and provides methods for adding, finding, and updating users.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.

        Creates a new instance of the DB class and sets up the database engine and session.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.

        Returns a memoized session object for interacting with the database.
        If the session object does not exist, it creates a new one.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.

        Args:
            email: The email of the user.
            hashed_password: The hashed password of the user.

        Returns:
            The newly created User object.

        Raises:
            Exception: If an error occurs while adding the user to the database.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user based on a set of filters.

        Args:
            **kwargs: Keyword arguments representing the filters to apply.

        Returns:
            The User object that matches the filters.

        Raises:
            InvalidRequestError: If an invalid filter is provided.
            NoResultFound: If no user is found that matches the filters.
        """
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        result = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user based on a given id.

        Args:
            user_id: The id of the user to update.
            **kwargs: Keyword arguments representing the fields to update and their new values.

        Raises:
            ValueError: If an invalid field is provided.
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        update_source = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                update_source[getattr(User, key)] = value
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            update_source,
            synchronize_session=False,
        )
        self._session.commit()