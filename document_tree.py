
class Node:
    def __init__(self, data : str, parent : 'Node') -> None:
        self.parent : 'Node' = parent
        self.childern : list['Node'] = list()
        self.data : str = data
    
    def __repr__(self) -> str:
        return f"(id : {id(self)}\ndata: {self.data}\nparent:{id(self.parent)}\n\tamount:{len(self.childern)})\n"

    def add_child(self, node : 'Node'):
        self.childern.append(node)

class Document:
    def __init__(self, name: str) -> None:
        self.root = Node(name, None)
    
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