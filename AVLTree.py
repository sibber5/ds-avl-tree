#id1: 213856032
#name1: Nara Zangariya
#username1: naraz
#id2: 213513443
#name2: Ghassan Jadoun
#username2: ghassanj

from typing import Self, Tuple


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node. creates virtual node if None is passed.
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key: int, value: str, leftNode: Self = None, rightNode: Self = None):
		if key is None:
			self.key = None
			self._parent = None
			self._height = -1
		else:
			self.key = key
			self.value = value
			self._left = None
			self._right = None
			self._parent = None
			self._height = 0

			self.left = leftNode
			self.right = rightNode

	@classmethod
	def virtual(cls):
		return cls(None, None)

	@property
	def left(self) -> Self:
		self._raise_if_virtual_node()
		return self._left
	
	@left.setter
	def left(self, val: (Self | None)):
		self._raise_if_virtual_node()
		if val is None:
			# when constructing
			if self._left is None:
				self._left = AVLNode.virtual()
				return

			if not self._left.is_real_node:
				return
			
			val = AVLNode.virtual()
		
		self._left._set_parent(None)
		self._left = val
		val._set_parent(self)
	

	@property
	def right(self) -> Self:
		self._raise_if_virtual_node()
		return self._right
	
	@right.setter
	def right(self, val: (Self | None)):
		self._raise_if_virtual_node()
		if val is None:
			# when constructing
			if self._right is None:
				self._right = AVLNode.virtual()
				return
			
			if not self._right.is_real_node:
				return
			
			val = AVLNode.virtual()
		
		self._right._set_parent(None)
		self._right = val
		val._set_parent(self)


	@property
	def parent(self):
		return self._parent
	
	def _set_parent(self, val: (Self | None)):
		if val is not None and not val.is_real_node:
			raise ValueError("Node parent cannot be a virtual node.")
		
		self._parent = val
		AVLNode._update_parent_heights(self)


	@property
	def height(self):
		if self._height != self.compute_height():
			raise ValueError("Node height value is incorrect.")
		return self._height


	"""
	@returns: (height of left node) - (height of right node).
	"""
	@property
	def balance_factor(self):
		self._raise_if_virtual_node()
		return self.left.height - self.right.height


	"""
	@returns: False if self is a virtual node, True otherwise.
	"""
	@property
	def is_real_node(self):
		return self.key is not None
	

	def _raise_if_virtual_node(self):
		if not self.is_real_node:
			raise RuntimeError("Invalid operation on virtual node.")

	
	# TODO: remove before submitting
	def compute_height(self) -> int:
		if not self.is_real_node:
			return -1
		
		return max(self.left.compute_height(), self.right.compute_height()) + 1


	@staticmethod
	def _update_parent_heights(node: Self):
		node = node.parent
		while node is not None:
			new_height = max(node.left.height, node.right.height) + 1
			if node._height == new_height:
				break
			node._height = new_height
			node = node.parent


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key: int) -> Tuple[AVLNode, int]:
		return AVLTree._search_rec(self.root, 1, key)

	@staticmethod
	def _search_rec(node: AVLNode, e: int, key: int):
		if node is None:
			return None, e

		if node.key == key:
			return node, e

		if node.key > key:
			return AVLTree._search_rec(node.left, e + 1, key)

		return AVLTree._search_rec(node.right, e + 1, key)


	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key: int) -> Tuple[AVLNode, int]:
		return None, -1


	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key: int, val: str) -> Tuple[AVLNode, int, int]:
		return None, -1, -1


	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key: int, val: str) -> Tuple[AVLNode, int, int]:
		return None, -1, -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node: AVLNode):
		return	

	
	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	def join(self, tree2: Self, key: int, val: str):
		return


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node: AVLNode) -> Tuple[Self, Self]:
		return None, None

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self) -> list:
		return None


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self) -> AVLNode:
		return None

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self) -> int:
		return -1	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self) -> AVLNode:
		return None
