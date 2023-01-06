"""
    Methods for finding likely YINL language constructs from a piece of text
"""

import re

MACRO_PATTERN = r"[a-zA-Z\-_]{1,50}: {0,1}\([a-zA-Z0-9\,. -/]*\)"
SECTION_START_PATTERN = r"section [A-Za-z0-9?!. ]*:(?! {0,1}\(.*)"

def find_macros(text: str) -> list[re.Match]:
    """
        Finds likely macros within a piece of text,
        returns a list of regex match objects
    """
    return list(re.finditer(MACRO_PATTERN, text))

def find_sections(text: str) -> list[re.Match]:
    """
        Finds likely sections within a piece of text,
        returns a list of regex match objects
    """
    return list(re.finditer(SECTION_START_PATTERN, text))