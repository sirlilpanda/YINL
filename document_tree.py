"""
    Defines nodes of the YINL document tree.
"""

import re

from typing import Callable, Union
from types import FunctionType
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
        tab_space_amount = 4 #TODO allow for differnt tab amounts
        lines = text.splitlines()
        #incase someone writes "comments" at the top of the file
        start_index = lines.index("header:")
        lines = list(filter( 
            None, #removes any empty strings
            map(
                lambda str: str[tab_space_amount:], #removes the first tab from all strings
                lines[start_index+1:] #plus one here so start string is not included in the lines
            )
        ))
        current_key = "" #current key that is values are related too
        for line in lines:
            # adds the setting as a key in the dict and strips the colon
            if line.endswith(":") or line.endswith(")") and not line.endswith("\\:") and not line.startswith(" "*tab_space_amount):
                current_key = line.strip(":")
                self.header.setdefault(current_key, [])
            # checks to see if the value is on the same line
            # this assumes that there is only one value
            elif ":" in line and "\:" not in line and not line.startswith(" "*tab_space_amount):
                key, val = line.split(":", 1)
                self.header.setdefault(key, [val.lstrip()])
            else:
                # add the value to the current key
                self.header[current_key] += [line.lstrip()]

    def parse_footer(self, text: str):
        """
            Parses the document footer from an open file.
        """
        tab_space_amount = 4 #TODO allow for differnt tab amounts
        lines = text.splitlines()
        #incase someone writes "comments" at the top of the file
        start_index = lines.index("footer:")
        lines = list(filter( 
            None, #removes any empty strings
            map(
                lambda str: str[tab_space_amount:], #removes the first tab from all strings
                lines[start_index+1:] #plus one here so start string is not included in the lines
            )
        ))
        # print(*lines, sep="\n")
        current_key = ""
        for line in lines:

            if not line.startswith(" "*tab_space_amount):
                current_key = line
                self.footer.setdefault(current_key, "")
            else:
                #remove the second tab
                self.footer[current_key] += line[4:]+"\n"

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
        macros = self.footer["macros:"]
        self.footer.pop("macros:")
        current_key = ""
        macros_dict = {}

        for line in (macros.splitlines()):
            if not line.startswith(" "*tab_space_amount):
                current_key = line
                macros_dict.setdefault(current_key, "")
            else:
                #remove the second tab
                macros_dict[current_key] += line+"\n"

        for func_name_n_args, func_body in macros_dict.items():
            f_name = func_name_n_args.split(":")[0]
            f_args = func_name_n_args.split(":")[1].strip()[1:-1].split(",")
            self.macros.setdefault(
                f_name,
                Document._convert_macro_string_to_func(func_body, f_name, f_args)        
            )
    
    @staticmethod
    def _convert_macro_string_to_func(func_body: str, func_name: str, func_args : list[str]) -> Callable:
        func = f"""def {func_name}({",".join(func_args)}):\n{func_body}"""
        code_obj = compile(func, '<string>', 'exec')
        return FunctionType(code_obj.co_consts[0], globals())


    def _parse_shorthands(self):
        """
            Parses the the shorthands from the footer in their own dict to be used
            in the parse_body method
        """
        for key, val in map(lambda s: s.split(":"), self.footer["shorthands:"].splitlines()):
            self.shorthands.setdefault(key.strip(), val.strip())
        self.footer.pop("shorthands:")

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
                    sections[-1].add_child(line.lstrip())

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
    
    def md(self) -> str:
        auth_sep = ",\n"
        out_str = f'''
# {self.header['title'][0]}
{"author" if len(self.header["authors"]) == 1 else "authors"}:{auth_sep.join(self.header["authors"])}
{self.header["date"][0]}
---\n
'''
        def body_to_str(section: Section, header_depth=2) -> str:
            body_str = ""
            body_str += "#"*header_depth+" "+section.name+"\n"
            for s in section.children:
                if type(s) == str:
                    if s:
                        body_str += s
                else:
                    body_str += body_to_str(s, header_depth+1)
                    body_str += "\n"+"#"*(header_depth+1)+"\n"
            return body_str

        for section in self.body:
            out_str += body_to_str(section)
        with open(f"{self.header['title'][0]}.md", "w+") as md:
            md.write(out_str)
        return out_str