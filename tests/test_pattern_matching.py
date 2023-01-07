"""
    Pytest tests for testing pattern matching module.
"""

from ..pattern_matching import *

with open("tests/test.yi", "r") as f:
    EXAMPLE_TEXT = f.read()
    EXAMPLE_NUM_MACROS = 6
    EXAMPLE_NUM_SECTIONS = 2
    EXAMPLE_NUM_SHORTANDS = 1

def test_get_indent():
    assert get_indent("    a") == 4
    assert get_indent("a") == 0
    assert get_indent(" a") == 1
    assert get_indent("") == 0
    assert get_indent("a    ") == 0

def test_locate_header():
    header = locate_header(EXAMPLE_TEXT)

    assert header.start() == 0
    assert header.end() == 179

def test_locate_footer():
    footer = locate_footer(EXAMPLE_TEXT)

    assert footer.start() == 613
    assert footer.end() == 827

def test_locate_macros():
    assert len(locate_macros(EXAMPLE_TEXT)) == EXAMPLE_NUM_MACROS

def test_locate_sections():
    sections = locate_sections(EXAMPLE_TEXT)
    assert len(sections) == EXAMPLE_NUM_SECTIONS

def test_locate_shorthands():
    assert len(locate_shorthands(EXAMPLE_TEXT)) == EXAMPLE_NUM_SHORTANDS