0x03. User authentication service

""In the industry, you should not implement your own authentication system and use a module or framework that doing it for you (like in Python-Flask: Flask-User). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.""

Learning Objectives
At the end of this project, you are expected to be able to explain to anyone, without the help of Google:

How to declare API routes in a Flask app
How to get and set cookies
How to retrieve request form data
How to return various HTTP status codes

Tasks
0. User model
In this task you will create a SQLAlchemy model named User for a database table named users (by using the mapping declaration of SQLAlchemy).

The model will have the following attributes:

id, the integer primary key
email, a non-nullable string
hashed_password, a non-nullable string
session_id, a nullable string
reset_token, a nullable string

1. create user
In this task, you will complete the DB class provided below to implement the add_user method.
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base


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
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
Note that DB._session is a private property and hence should NEVER be used from outside the DB class.

Implement the add_user method, which has two required string arguments: email and hashed_password, and returns a User object. The method should save the user to the database. No validations are required at this stage.

2. Find user
In this task you will implement the DB.find_user_by method. This method takes in arbitrary keyword arguments and returns the first row found in the users table as filtered by the method’s input arguments. No validation of input arguments required at this point.

Make sure that SQLAlchemy’s NoResultFound and InvalidRequestError are raised when no results are found, or when wrong query arguments are passed, respectively.

Warning:

NoResultFound has been moved from sqlalchemy.orm.exc to sqlalchemy.exc between the version 1.3.x and 1.4.x of SQLAchemy - please make sure you are importing it from sqlalchemy.orm.exc

3. update user
In this task, you will implement the DB.update_user method that takes as argument a required user_id integer and arbitrary keyword arguments, and returns None.

The method will use find_user_by to locate the user to update, then will update the user’s attributes as passed in the method’s arguments then commit changes to the database.

If an argument that does not correspond to a user attribute is passed, raise a ValueError.


4. Hash password.
In this task you will define a _hash_password method that takes in a password string arguments and returns bytes.

The returned bytes is a salted hash of the input password, hashed with bcrypt.hashpw.

5. Register user
In this task, you will implement the Auth.register_user in the Auth class provided below:
from db import DB


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
Note that Auth._db is a private property and should NEVER be used from outside the class.

Auth.register_user should take mandatory email and password string arguments and return a User object.

If a user already exist with the passed email, raise a ValueError with the message User <user's email> already exists.

If not, hash the password with _hash_password, save the user to the database using self._db and return the User object.

6. Basic Flask app
In this task, you will set up a basic Flask app.

Create a Flask app that has a single GET route ("/") and use flask.jsonify to return a JSON payload of the form:

{"message": "Bienvenue"}
Add the following code at the end of the module:

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

7. Register user
In this task, you will implement the end-point to register a user. Define a users function that implements the POST /users route.

Import the Auth object and instantiate it at the root of the module as such:

from auth import Auth


AUTH = Auth()
The end-point should expect two form data fields: "email" and "password". If the user does not exist, the end-point should register it and respond with the following JSON payload:

{"email": "<registered email>", "message": "user created"}
If the user is already registered, catch the exception and return a JSON payload of the form

{"message": "email already registered"}
and return a 400 status code

Remember that you should only use AUTH in this app. DB is a lower abstraction that is proxied by Auth.