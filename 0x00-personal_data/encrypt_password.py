#!/usr/bin/env python3
"""Encript a password."""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate a password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
