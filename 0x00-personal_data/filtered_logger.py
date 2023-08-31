#!/usr/bin/env python3
"""Obfuscate personal data."""


from typing import List
import re
import logging

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize a RedactingFormatter class."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Obfuscate a log message."""
        return filter_datum(self.fields,
                            self.REDACTION,
                            super().format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Create a Logger instance."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    logger.propagate = False
    return logger
