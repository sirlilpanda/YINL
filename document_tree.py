"""
    Defines nodes of the YINL document tree.
"""

from typing import Callable
from dataclasses import dataclass

class Node:
    def __init__(self, data : str, parent : 'Node' = None) -> None:
        self.parent : 'Node' = parent
        self.children : list['Node'] = list()
        self.data : str = data
    
    def __repr__(self) -> str:
        return f"(id : {id(self)}\ndata: {self.data}\nparent:{id(self.parent)}\n\tamount:{len(self.children)})\n"

    def add_child(self, node : 'Node'):
        node.parent = self
        self.children.append(node)

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

    def __init__(self, name: str) -> None:
        self.header = Header(self)
        self.root = Node(name)
        self.footer = Footer(self)

    def parse_header(self, file: str) -> None:
        """
            Parses the document header from an open file.
        """
        lines = file.split("\n")
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
            elif ":" in line:
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
    
    def parse_file(self, file: str):
        self.parse_header(file)
        raw_file : list[str] = file.split("\n")
        current = self.root
        last_depth = 0
        for line in raw_file:
            line = line.split(" "*4)
            depth_amount = len(line)-1
            if last_depth == depth_amount:
                last_depth += 1
            elif last_depth > depth_amount:
                for _ in range(depth_amount+1):
                    current = current.parent                
                last_depth -= depth_amount
            node = Node(
                line.pop(),
                current
            )
            current.add_child(node)
            current = node
    
    def __repr__(self) -> str:
        return str(self.root)