"""
    Defines nodes of the YINL document tree.
"""

import re

from typing import Callable, Union
from pattern_matching import locate_header, locate_footer, SECTION_START_PATTERN

class Section:
    """
        Describes a section of the body of the document.

        Parameters
        ----------

        name: str
            The name (title) of the section.
        indent: int
            The indent level of the section
        parent: Section
            The parent section of this section. May be None if no parent.
        pos: int
            The position of this section within its parent section. Defaults to 0.
    """
    def __init__(self, name: str, indent: int = 0, parent: 'Section' = None, pos: int = 0) -> None:
        self.name: str = name
        self.indent: int = indent
        self.parent: 'Section' = parent
        self.pos: int = pos
        self.children: list[Union['Section', str]] = list()
    
    def __repr__(self) -> str:
        
        return f"Section({self.name}, {self.children})"

    def add_child(self, section: Union['Section', str]):
        if isinstance(section, Section):
            section.parent = self
        self.children.append(section)

class Document:
    """
        Describes a YINL document.
        Produced with `Document().parse_file("path/to/file.yi")`
    """

    def __init__(self) -> None:
        self.header : dict[str, list[str]] = dict() 
        self.body: list[Section] = []
        # citations and appendix should really only exist in here
        self.footer : dict[str, list[str]] = dict() 
        self.macros : dict[str, Callable] = dict()
        self.shorthands : dict[str, str] = dict()

    def __repr__(self) -> str:

        return "\n".join(str(section) for section in self.body)

    def parse_header(self, text: str):
        """
            Parses the document header from an open file.
        """
        self.header = Document._parse_text_to_dict("header:", text)
    def parse_footer(self, text: str):
        """
            Parses the document footer from an open file.
        """
        self.footer = Document._parse_text_to_dict("footer:", text)
        # removes the macros from the footer dict and does further processing
        self._parse_macros()
        self._parse_shorthands()
        #cleans up the strings of the citations and other settings
        for k in self.footer.keys():
             self.footer[k] = list(map(str.strip, self.footer[k]))
    
    def _parse_macros(self):
        """
            Parses the macros from the footer with some futher processing
        """
        tab_space_amount = 4
        macros = self.footer["macros"]
        current_key = ""
                    # removes the first nest of tabs
        for line in map(lambda s: s[4:], macros):
            if not line.startswith(" "*tab_space_amount):
                current_key = line.split(":")[0]
                self.macros.setdefault(current_key, "")
            else:
                #remove the second tab
                self.macros[current_key] += line[4:]+"\n"
        self.footer.pop("macros")


    def _parse_shorthands(self):
        """
            Parses the the shorthands from the footer in their own dict to be used
            in the parse_body method
        """
        for key, val in map(lambda s: s.split(":"), self.footer["shorthands"]):
            self.shorthands.setdefault(key.strip(), val.strip())
        self.footer.pop("shorthands")

    @classmethod
    def _parse_text_to_dict(cls, start_str: str, text: str) -> dict[str, str]:
        """
            parses the tabbed scoped text in to a dict
        """
        tab_space_amount = 4 #TODO allow for differnt tab amounts
        lines = text.splitlines()
        #incase someone writes "comments" at the top of the file
        start_index = lines.index(f"{start_str}") if start_str else 0
        lines = list(filter( 
            None, #removes any empty strings
            map(
                lambda str: str[tab_space_amount:], #removes the first tab from all strings
                lines[start_index+1:] #plus one here so start string is not included in the lines
            )
        ))
        return_dict = {}
        current_key = "" #current key that is values are related too
        for line in lines:
            # adds the setting as a key in the dict and strips the colon
            if line.endswith(":") or line.endswith(")") and not line.endswith("\\:") and not line.startswith(" "*tab_space_amount):
                current_key = line.strip(":")
                return_dict.setdefault(current_key, [])
            # checks to see if the value is on the same line
            # this assumes that there is only one value
            elif ":" in line and "\:" not in line and not line.startswith(" "*tab_space_amount):
                key, val = line.split(":", 1)
                return_dict.setdefault(key, [val.lstrip()])
            else:
                # add the value to the current key
                return_dict[current_key] += [line.lstrip()]
        return return_dict


    def parse_body(self, text: str):
        """
            Parses the body of the open file.
        """

        lines = text.splitlines()
        sections = []

        for line in lines:

            if re.match(SECTION_START_PATTERN, line.strip()) is not None:
                # identify section start
                curr_section = Section(line.strip()[8:-1], len(line) - len(line.lstrip()))

                # if we have already found a section
                if len(sections) > 0:
                    prev_section = sections[-1]
                    prev_section.add_child(curr_section)
                else:
                    self.body.append(curr_section)

                sections.append(curr_section)

            elif len(sections) > 0:
                # if section identified
                last_section = sections[-1]
                indent = len(line) - len(line.lstrip())

                if line.strip() == "":
                    last_section.add_child("\n")
                elif indent > last_section.indent:
                    last_section.add_child(line.lstrip())
                else:
                    sections.pop()

        # TODO: implement macros and shorthands


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