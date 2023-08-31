#!/usr/bin/env python3
"""Encript a password."""

import bcrypt


def hash_password(password: str) -> byte:
    """Hash a password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
