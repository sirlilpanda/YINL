"""
    Defines nodes of the YINL document tree.
"""

import re

from typing import Callable
from dataclasses import dataclass 

from pattern_matching import locate_header, locate_footer, locate_macros, locate_sections, locate_shorthands

@dataclass
class Header:
    """
        Stores document header information as per YINL spec.
        This is meant to be a direct reflection of the document header in the YINL file.
    """
    document: 'Document'
    title: str = None
    authors: list[str] = None
    date: str = None
    institute: str = None
    citation_style: str = None      

class Section:
    """
        Describes a section of the body of the document.

        Parameters
        ----------

        name: str
            The name (title) of the section.
        content: str
            The content of the section.
        parent: Section
            The parent section of this section. May be None if no parent.
        pos: int
            The position of this section within its parent section. Defaults to 0.
    """
    def __init__(self, name: str, content: str, parent: 'Section' = None, pos: int = 0) -> None:
        self.name: str = name
        self.content: str = content
        self.parent: 'Section' = parent
        self.pos: int = pos
        self.children: list['Section'] = list()
    
    def __repr__(self) -> str:
        
        return f"Section({self.name}, {self.content})"

    def add_child(self, section: 'Section'):
        section.parent = self
        self.children.append(section)

@dataclass
class Footer:
    """
        Stores document footer information as per YINL spec.
        This is meant to be a direct reflection of the document footer in the YINL file.
    """
    document: 'Document'
    citations: dict[str, str] = None
    macros: dict[str, Callable] = None
    shorthands: dict[str, str] = None

class Document:
    """
        Describes a YINL document.
        Produced with `Document().parse_file("path/to/file.yi")`
    """

    def __init__(self) -> None:
        self.header = Header(self)
        self.body: list[Section] = []
        self.footer = Footer(self)

    def __repr__(self) -> str:

        return "\n".join(str(section) for section in self.body)

    def parse_header(self, text: str):
        """
            Parses the document header from an open file.
        """
        lines = text.splitlines()
        header_start = lines.index("header:")
        header_end = lines[header_start:].index("")
        header_lines = [line.strip() for line in lines[header_start:header_end] if line != ""]

        i = 0
        while i < len(header_lines):
            line = header_lines[i]

            if line.endswith(":") and not line.endswith("\\:"):
                # key with value on next line
                key = line[:-1]
                value = header_lines[i+1]
                i += 1 # skip value line
            elif ":" in line and "\:" not in line:
                # key with value on same line
                key, value = line.split(":")
                value = value.strip()
            else:
                # not a key!
                # so skip
                i += 1
                continue
            
            if key == "author": #as there maybe more then one author setting
                self.header.__setattr__(key, [author.strip() for author in value.split(",")])
            else:
                self.header.__setattr__(key, value)
            i += 1

    def parse_footer(self, text: str):
        """
            Parses the document header from an open file.
        """
        footer_start = text.splitlines().index("footer:")
        # TODO: implement

    def parse_body(self, text: str):
        """
            Parses the body of the open file.
        """
        sections = locate_sections(text)
        macros = locate_macros(text)
        shorthands = locate_shorthands(text)

        for section in sections:
            # TODO: parse out subsections and mark them as a child of the parent section
            self.sections.append(Section(section[0], section[1]))

        # TODO: deal with macros and shorthands
        # may need to parse the footer first in order to implement this

    def parse_text(self, text: str):
        """
            Parses text into a document tree
        """
        header = locate_header(text)
        footer = locate_footer(text)

        self.parse_header(text[header.start():header.end()])
        self.parse_footer(text[footer.start():footer.end()])
        self.parse_body(text[header.end():footer.start()])

    def parse_file(self, file: str):
        """
            Parses text from a .yi file into a document tree
        """
        with open(file, "r") as f:
            text = f.read()
        self.parse_text(text)