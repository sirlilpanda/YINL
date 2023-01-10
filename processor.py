from pprint import pprint
import re
from document_tree import Document

def load_file(filename) -> str:
    with open(filename, "r+") as txt:
        return txt.read()

def main():
    file = load_file("example.yi")    
    doc = Document()
    doc.parse_text(file)
    print(doc.header)
    print(doc)

if __name__ == "__main__":
    main()