#!/usr/bin/env python3
"""BasicAuth class module."""


from api.v1.auth.auth import Auth
from base64 import b64decode, binascii
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """A class for Basic Access Authentication."""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract the base64 auth header."""
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None

        start_str = authorization_header.split(" ")[0]
        if start_str != "Basic":
            return None

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           authorization_header: str) -> str:
        """Decode a base64 authorization header."""
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None

        try:
            return b64decode(authorization_header).decode('utf-8')
        except binascii.Error as e:
            return None

    def extract_user_credentials(self,
                                 authorization_header: str) -> (str, str):
        """Etract user's credentials from authorization header."""
        if not authorization_header:
            return None, None
        if not isinstance(authorization_header, str):
            return None, None
        if ':' not in authorization_header:
            return None, None
        delimeter_index = authorization_header.index(':')
        email = authorization_header[0:delimeter_index]
        password = authorization_header[delimeter_index + 1:]
        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return a User instance based on email and password."""
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            user_list = User.search({"email": user_email})
            if not user_list:
                return None
            for user in user_list:
                return user if user.is_valid_password(user_pwd) else None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve a User instance for a request."""
        auth_header = self.authorization_header(request)
        auth_h_enc = self.extract_base64_authorization_header(auth_header)
        auth_h_dec = self.decode_base64_authorization_header(auth_h_enc)
        email, password = self.extract_user_credentials(auth_h_dec)
        user = self.user_object_from_credentials(email, password)
        return user
