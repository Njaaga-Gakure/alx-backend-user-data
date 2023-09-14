#!/usr/bin/env python3
"""Encript a password."""


import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """Encrypt a password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a unique id."""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Instatantiate an auth object."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user."""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Authenticate a user."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  getattr(user, 'hashed_password'))
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a session."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            setattr(user, 'session_id', session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get user from session id."""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a session."""
        try:
            user = self._db.find_user_by(id=user_id)
            setattr(user, 'session_id', None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Get a reset password token."""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            setattr(user, 'reset_token', reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError
