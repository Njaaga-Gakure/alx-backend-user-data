#!/usr/bin/env python3
"""Auth class module."""


from flask import request
from typing import List, TypeVar


class Auth:
    """A class to handle authetication."""

    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """Check if route requires authemtication."""
        if not path or not excluded_paths:
            return True
        if path[len(path) - 1] != "/":
            path = path + "/"
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Get the Authorization in the headers of the reuest."""
        if not request:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Handle later."""
        return None
