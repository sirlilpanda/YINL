"""
    Defines nodes of the YINL document tree.
"""

import re

from typing import Callable
from dataclasses import dataclass 

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
    """
    def __init__(self, name: str, content: str, parent : 'Section' = None) -> None:
        self.parent: 'Section' = parent
        self.name: str = name
        self.children: list['Section'] = list()
        self.content: str = content
    
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

    def __init__(self) -> None:
        self.header = Header(self)
        self.body: list[Section] = []
        self.footer = Footer(self)

    def __repr__(self) -> str:

        return "\n".join(str(section) for section in self.body)

    def parse_header(self, lines: list[str]) -> tuple[int, int]:
        """
            Parses the document header from an open file.
            Returns the index of the header start and end in the file
        """
        header_start = lines.index("header:")
        header_end = lines[header_start:].index("")
        header_lines = [line.strip() for line in lines[header_start:header_start+header_end] if line != ""]

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

            match key:
                case "title":
                    self.header.title = value
                case "author":
                    self.header.authors = [author.strip() for author in value.split(",")]
                case "date":
                    self.header.date = value
                case "institute":
                    self.header.institute = value
                case "citations":
                    self.header.citation_style = value

            i += 1

        return header_start, header_end

    def parse_footer(self, lines: list[str]) -> tuple[int, int]:
        """
            Parses the document header from an open file.
            Returns the index of the header start and end in the file
        """
        return 0, 0

    def parse_body(self, lines: list[str]) -> tuple[int, int]:
        """
            Parses the body of the open file.
        """
        i = 0
        content = []
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("section") and line.endswith(":"):
                content = []
                section = Section(line[7:-1].strip(), content)
                self.body.append(section)
            elif line.startswith("footer:"):
                # end of body
                return 0, i
            else:
                content.append(line)
            i += 1
        # end of body, no footer
        return 0, -1

    def parse_file(self, file: str):
        """
            Parses an open file into a Document tree.
        """
        lines = file.split("\n")
        _, header_end = self.parse_header(lines)
        _, body_end = self.parse_body(lines[header_end:])
        if body_end != -1:
            _, _ = self.parse_footer(lines[header_end+body_end:])