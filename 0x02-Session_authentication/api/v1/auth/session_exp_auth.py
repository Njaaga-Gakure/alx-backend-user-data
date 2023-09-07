#!/usr/bin/env pyrhon3
"""session expiry authentication module."""


from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """A class that reps session auth with expiry."""

    def __init__(self):
        """Instantiate a SessionExpAuth object."""
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {"user_id": user_id,
                              "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve a user_id based on a session_id."""
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        if "created_at" not in session_dict.keys():
            return None
        if ((session_dict.get("created_at")
                + timedelta(seconds=self.session_duration) < datetime.now())):
            return None
        return session_dict.get("user_id")
