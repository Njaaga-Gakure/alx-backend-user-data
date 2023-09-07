#!/usr/bin/env python3
"""Session Authntication Module."""


from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """A class to handle session authentication."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session.

        args:
            user_id (str): id of a user
        returns:
            the session id

        """
        if not user_id:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve a user_id based on a session_id.

        args:
            session_id (str): session id
        returns:
            a user id based on a session id

        """
        if not session_id:
            return None
        if not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """Get user based on a sessio id."""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroy a session."""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True
