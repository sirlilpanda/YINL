"""
    Methods for finding likely YINL language constructs from a piece of text
"""

import re

from math import gcd
from functools import reduce

MACRO_PATTERN = r"[a-zA-Z\-_]{1,50}: {0,1}\([a-zA-Z0-9\,. -/]*\)"
SECTION_START_PATTERN = r" *section .*: {0,1}(?! {0,1}\(.*)"
ROOT_SECTION_START_PATTERN = r"section .*: {0,1}(?! {0,1}\(.*)"
SHORTHAND_PATTERN = r" .*\\[a-zA-Z\-_] "
HEADER_PATTERN = r"header:.*?(?=\nsection)"
FOOTER_PATTERN = r"footer:.*?$"

def locate_header(text: str) -> re.Match:
    """
        Locates the header within the document.
    """
    return re.search(HEADER_PATTERN, text, re.DOTALL)

def locate_footer(text: str) -> re.Match:
    """
        Locates the footer within the document.
    """
    return re.search(FOOTER_PATTERN, text, re.DOTALL)

def locate_macros(text: str) -> list[re.Match]:
    """
        Finds likely macro posiitons within a piece of text,
        returns a list of regex match objects
    """
    return list(re.finditer(MACRO_PATTERN, text))

def locate_sections(text: str) -> list[re.Match]:
    """
        Finds likely section positions within a piece of text,
        returns a list of regex match objects
    """
    return list(re.finditer(SECTION_START_PATTERN, text))

def locate_root_sections(text: str) -> list[re.Match]:
    """
        Finds likely sections in the body root,
        returns a list of regex match objects
    """
    return list(re.finditer(SECTION_START_PATTERN, text))

def locate_shorthands(text: str) -> list[re.Match]:
    """
        Finds likely shorthand positions within a piece of text,
        returns a list of regex match objects
    """
    return list(re.finditer(SHORTHAND_PATTERN, text))