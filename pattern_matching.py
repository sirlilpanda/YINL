"""
    Methods for finding likely YINL language constructs from a piece of text
"""

import re

from math import gcd
from functools import reduce

MACRO_PATTERN = r"[a-zA-Z\-_]{1,50}: {0,1}\([a-zA-Z0-9\,. -/]*\)"
SECTION_START_PATTERN = r" *section .*: {0,1}(?! {0,1}\(.*)"
SHORTHAND_PATTERN = r" .*\\[a-zA-Z\-_] "
HEADER_PATTERN = r"header:.*?(?=\nsection)"
FOOTER_PATTERN = r"footer:.*?$"

def get_indent(line: str) -> int:
    """
        Determines the size of the indent of a line.
    """
    return len(line) - len(line.lstrip())

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

def locate_shorthands(text: str) -> list[re.Match]:
    """
        Finds likely shorthand positions within a piece of text,
        returns a list of regex match objects
    """
    return list(re.finditer(SHORTHAND_PATTERN, text))

def get_header(text: str) -> str:
    """
        Gets the header from a piece of text.
    """
    return locate_header(text).group()

def get_footer(text: str) -> str:
    """
        Gets the footer from a piece of text.
    """
    return locate_footer(text).group()

def get_sections(text: str, matches: list[re.Match] = None) -> list[tuple[str, int, str]]:
    """
        Gets sections and their contents from a piece of text.
        Note that section content may include subsections, macros, and shorthands.
        Returns a list of tuples of the form (section_name, section_indent, section_content)

        Parameters
        ----------

        text: str
            The text to search
        matches: list[re.Match]
            A list of regex matches to use for section locations. If none supplied, will be found automatically.
    """
    if matches is None:
        section_locations = locate_sections(text)
    else:
        section_locations = matches
        
    indents = [get_indent(text[:section.end()].splitlines()[-1]) for section in section_locations]

    indent_size = reduce(gcd, indents)
    if indent_size == 0:
        indent_size = 4 # default to 4 spaces if no indent is found

    sections = []
    for section, indent in zip(section_locations, indents):

        section_name = section.group().strip().split(":")[0][7:].strip()
        section_indent = indent // indent_size

        # get the content of the section
        section_content = ""
        for line in text[section.end():].splitlines()[1:]:
            if get_indent(line) // indent_size > section_indent:
                # include lines that are indented more than the section
                section_content += line[(section_indent+1)*indent_size:].rstrip() + "\n"
            elif len(line) == 0:
                # inclue empty lines
                section_content += "\n"
            else:
                # break if the line is less indented than the section and is not empty
                # this indicates the section has ended :)
                break
        sections.append((section_name, section_indent, section_content))

    return sections
    
def get_macros(text: str) -> list[tuple[str, tuple[str]]]:
    """
        Gets macros and their arguments from a piece of text.
        Returns a list of tuples of the form (macro_name, macro_args)
    """
    macro_locations = locate_macros(text)
    macros = []
    for macro in macro_locations:
        macro_name = macro.group().split(":")[0].strip()
        macro_args = macro.group().split(":")[1].strip()[1:-1].split(",")
        macro_args = tuple([arg.strip() for arg in macro_args])
        macros.append((macro_name, macro_args))
    return macros