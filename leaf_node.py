from crypto import sha512Half
from shamap_node import node_type, shamap_node

HEX = 16

class leaf_node(shamap_node):
  def __init__(self, tag, data, type):
    self.tag = tag
    self.type = type
    self.data = data

  def addItem(tag, node):
    raise 'Cannot call addItem on a LeafNode'
  
  def removeItem(self, tag):
    raise 'Cannot call removeItem on a LeafNode'

  def hash(self):
    if self.type == node_type.ACCOUNT_STATE:
        leafPrefix = '4D4C4E00'
        return sha512Half(leafPrefix + self.data + self.tag)
        
    elif self.type == node_type.TRANSACTION_NO_METADATA:
        txIDPrefix = '54584E00'
        return sha512Half(txIDPrefix + self.data)

    elif self.type == node_type.TRANSACTION_METADATA:
        txNodePrefix = '534E4400'
        return sha512Half(txNodePrefix + self.data + self.tag)
      
    raise 'Tried to hash a SHAMap node of unknown type.'