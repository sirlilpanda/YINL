"""
    Pytest tests for testing pattern matching module.
"""

from ..pattern_matching import find_macros, find_sections

with open("tests/test.yi", "r") as f:
    EXAMPLE_TEXT = f.read()
    EXAMPLE_NUM_MACROS = 6
    EXAMPLE_NUM_SECTIONS = 2

def test_find_macros():
    assert len(find_macros(EXAMPLE_TEXT)) == EXAMPLE_NUM_MACROS

def test_find_sections():
    assert len(find_sections(EXAMPLE_TEXT)) == EXAMPLE_NUM_SECTIONS