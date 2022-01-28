from itertools import accumulate
from crypto import sha512Half
from leaf_node import leaf_node
from shamap_node import node_type, shamap_node

HEX_ZERO = '0000000000000000000000000000000000000000000000000000000000000000'

SLOT_MAX = 16
HEX = 16

class inner_node(shamap_node):
  def countLeaves(self):
    count = 0
    for i in range(16):
      if self.leaves[i] != None:
        count += 1
    return count

  def empty(self):
    return self.countLeaves() == 0

  def __init__(self, depth):
    self.leaves = [None for i in range(16)]
    self.type = node_type.INNER
    self.depth = depth

  def addItem(self, tag: str, node: shamap_node):
    existingNode = self.getNode(int(tag[self.depth], base=16))

    if existingNode == None:
      self.setNode(int(tag[self.depth], base=16), node)
      return

    # A node already exists in this slot
    if isinstance(existingNode, inner_node):
      # There is an inner node, so we need to go deeper
      existingNode.addItem(tag, node)
    else:
      if existingNode.tag == tag:
        # Collision
        raise 'Tried to add a node to a SHAMap that was already in there.'
      else:
        newInnerNode = inner_node(self.depth + 1)

        # Parent new and existing node
        newInnerNode.addItem(existingNode.tag, existingNode)
        newInnerNode.addItem(tag, node)

        # And place the newly created inner node in the slot
        self.setNode(int(tag[self.depth], base=16), newInnerNode)

  def removeItem(self, tag):
      existingNode = self.getNode(int(tag[self.depth], base=16))

      if existingNode == None:
        raise 'No node exists at ' + tag

      if isinstance(existingNode, inner_node):
        existingNode.removeItem(tag)

        ## if its empty, remove the inner node
        if existingNode.countLeaves() == 0:
          self.setNode(int(tag[self.depth], base=16), None)

        if existingNode.countLeaves() == 1:
          self = existingNode


      else: #instanceof leaf_node
        if existingNode.tag != tag:
          raise 'tag does not match existing node tag'
        else:
          self.setNode(int(tag[self.depth], base=16), None)

  def setNode(self, slot: int, node: shamap_node):
    if slot < 0 or slot > SLOT_MAX:
      raise 'Invalid slot: slot must be between 0-15.'
    
    self.leaves[slot] = node
  
  def getNode(self, slot: int):
    if slot < 0 or slot > SLOT_MAX:
      raise 'Invalid slot: slot must be between 0-15.'
    
    return self.leaves[slot]

  def hash(self) -> str: 
    if (self.empty()):
      return HEX_ZERO

    hex = ''
    for iter in range(SLOT_MAX):
      child = self.leaves[iter]
      hash = HEX_ZERO if child == None else child.hash()
      hex += hash

    prefix = '4D494E00'
    return sha512Half(prefix + hex)
