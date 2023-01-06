"""
    Pytest tests for testing pattern matching module.
"""

from ..pattern_matching import find_macros

with open("tests/test.yi", "r") as f:
    EXAMPLE_TEXT = f.read()
    EXAMPLE_NUM_MACROS = 6

def test_find_macros():

    found_macros = find_macros(EXAMPLE_TEXT)
    print(found_macros)
    assert len(found_macros) == EXAMPLE_NUM_MACROS