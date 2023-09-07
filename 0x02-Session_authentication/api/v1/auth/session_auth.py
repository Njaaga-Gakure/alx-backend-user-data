#!/usr/bin/env python3
"""Session Authntication Module."""


from api.v1.auth.auth import Auth
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
