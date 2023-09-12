#!/usr/bin/env python3
"""Encript a password."""


import bcrypt


def _hash_password(password: str) -> bytes:
    """Encrypt a password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
