#!/usr/bin/env python3
"""Obfuscate personal data."""


from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Obfuscate a user's personal data.

    args:
        fields (List[str]): field to obfuscate
        reduction (str): string to reduct the fields with
        message (str): the log line
        separator (str): character separating the field

    returns:
        obfusted message

    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         rf'{field}={redaction}{separator}', message)
    return message
