"""
    Pytest tests for testing pattern matching module.
"""

from ..pattern_matching import find_macros

with open("tests/test.yi", "r") as f:
    TEST_TEXT = f.read()

def test_find_macros():

    found_macros = find_macros(TEST_TEXT)
    print(found_macros)
    assert len(found_macros) == 6