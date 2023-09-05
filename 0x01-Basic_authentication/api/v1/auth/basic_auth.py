#!/usr/bin/env python3
"""BasicAuth class module."""


from api.v1.auth.auth import Auth


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
