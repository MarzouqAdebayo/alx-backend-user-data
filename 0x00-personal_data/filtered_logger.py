#!/usr/bin/env python3
"""Module 'filtered_logger.py' """
import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    pattern = f'({"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, lambda x: f"{x.group(1)}={redaction}", message)
