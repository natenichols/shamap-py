from inner_node import inner_node
from leaf_node import leaf_node

class shamap:
    def __init__(self):
        self.root = inner_node(0)

    def insert(self, tag, data, type):
        self.root.addItem(tag, leaf_node(tag, data, type))

    def erase(self, tag):
        self.root.removeItem(tag)

    def hash(self):
        return self.root.hash()