"""
    Pytest tests for testing pattern matching module.
"""

from ..pattern_matching import get_indent, locate_macros, get_macros, locate_sections, get_sections

with open("tests/test.yi", "r") as f:
    EXAMPLE_TEXT = f.read()
    EXAMPLE_NUM_MACROS = 6
    EXAMPLE_NUM_SECTIONS = 2

def test_get_indent():
    assert get_indent("    a") == 4
    assert get_indent("a") == 0
    assert get_indent(" a") == 1
    assert get_indent("") == 0
    assert get_indent("a    ") == 0

def test_locate_macros():
    assert len(locate_macros(EXAMPLE_TEXT)) == EXAMPLE_NUM_MACROS

def test_get_macros():
    macros = get_macros(EXAMPLE_TEXT)

    assert macros[0][0] == "anchor"      # name
    assert macros[0][1][0] == "why-yinl" # tag (arg)

    assert macros[1][0] == "figure"                          # name
    assert macros[1][1][0] == "/path/to/img.png"             # path (arg)
    assert macros[1][1][1] == "Figure 1 - An example figure" # caption (arg)

    assert len(macros) == EXAMPLE_NUM_MACROS

def test_locate_sections():
    assert len(locate_sections(EXAMPLE_TEXT)) == EXAMPLE_NUM_SECTIONS

def test_get_sections():
    sections = get_sections(EXAMPLE_TEXT)

    assert sections[0][0] == "Introduction" # title
    assert sections[0][1] == 0              # indent level
    
    assert sections[1][0] == "Why YINL?" # title
    assert sections[1][1] == 1           # indent level

    assert len(sections) == EXAMPLE_NUM_SECTIONS