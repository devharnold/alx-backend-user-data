#!/usr/bin/env python3
"""log message obfuscate model.
"""
from typing import field




def filter_datum(field: field, redaction: str, message: str, separator: str):
    """Function returns log message eobfuscated
    Attributes:
        fields: a list of strings representing all fields to obfuscate
        redaction: a list representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all fields"""
    for i in field:
        message = message.replace(i + separator, redaction + separator)
    return message