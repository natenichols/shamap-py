from enum import Enum

class node_type(Enum):
    INNER = 1,
    TRANSACTION_NO_METADATA = 2,
    TRANSACTION_METADATA = 3,
    ACCOUNT_STATE = 4,

class shamap_node:
    def addItem(self, tag, node):
        pass
    def removeItem(self, tag):
        pass
    def hash(self):
        pass
