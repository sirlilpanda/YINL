"""
    Defines nodes of the YINL document tree.
"""

from typing import Callable
from dataclasses import dataclass
from datetime import datetime

class Node:
    def __init__(self, data : str, parent : 'Node' = None) -> None:
        self.parent : 'Node' = parent
        self.children : list['Node'] = list()
        self.data : str = data
    
    def __repr__(self) -> str:
        return f"(id : {id(self)}\ndata: {self.data}\nparent:{id(self.parent)}\n\tamount:{len(self.childern)})\n"

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
    authors: list[str] = []
    date: datetime = None
    institute: str = None
    citation_style: str = None      

@dataclass
class Footer:
    """
        Stores document footer information as per YINL spec.
        This is meant to be a direct reflection of the document footer in the YINL file.
    """
    document: 'Document'
    citations: dict[str, str] = dict()
    macros: dict[str, Callable] = dict()
    shorthands: dict[str, str] = dict()

class Document:
    def __init__(self, name: str) -> None:
        self.header = Header(self)
        self.root = Node(name, None)
        self.footer = Footer(self)
    
    def parse_file(self, file:str):
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