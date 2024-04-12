#!/usr/bin/env python3
"""log message obfuscate model.
"""
from typing import field
import re


def filter_datum(fields, redaction, message, separator):
    """Function returns log message eobfuscated
    Attributes:
        fields: a list of strings representing all fields to obfuscate
        redaction: a list representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all fields"""
    return re.sub('|'.join(fields), redaction, message)