"""
    Methods for finding likely YINL language constructs from a piece of text
"""

import re

MACRO_PATTERN = r"[a-zA-Z\-_]{1,50}: {0,1}\([a-zA-Z0-9\,. -/]*\)"

def find_macros(text: str) -> list[tuple[int, int]]:
    """
        Finds likely macros within a piece of text,
        returns a list of regex match objects
    """
    return re.findall(MACRO_PATTERN, text, re.MULTILINE) 