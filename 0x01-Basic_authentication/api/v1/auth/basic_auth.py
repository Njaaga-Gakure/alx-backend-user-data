#!/usr/bin/env python3
"""BasicAuth class module."""


from api.v1.auth.auth import Auth
from base64 import b64decode, binascii


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
