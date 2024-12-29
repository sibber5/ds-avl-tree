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
    def __init__(self, key: int, value: str):
        if key is None:
            self.key = None
            self._parent = None
            self._height = -1
        else:
            self.key = key
            self.value = value
            self._left = AVLNode.virtual()
            self._left._parent = self
            self._right = AVLNode.virtual()
            self._right._parent = self
            self._parent = None
            self._height = 0

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
            if not self._left.is_real_node:
                return

            val = AVLNode.virtual()

        self._left._parent = None
        self._left = val
        _set_child_of_parent(val, None)
        val._parent = self
        self._update_heights()

    @property
    def right(self) -> Self:
        self._raise_if_virtual_node()
        return self._right

    @right.setter
    def right(self, val: (Self | None)):
        self._raise_if_virtual_node()
        if val is None:
            if not self._right.is_real_node:
                return

            val = AVLNode.virtual()

        self._right._parent = None
        self._right = val
        _set_child_of_parent(val, None)
        val._parent = self
        self._update_heights()

    @property
    def parent(self):
        return self._parent

    @property
    def height(self):
        assert self._height == self.compute_height()
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
            raise RuntimeError('Invalid operation on virtual node.')

    def _update_heights(self):
        while self is not None:
            new_height = max(self.left.height, self.right.height) + 1
            if self._height == new_height:
                return
            self._height = new_height
            self = self.parent

    # TODO: remove before submitting
    def compute_height(self) -> int:
        if not self.is_real_node:
            return -1

        return max(self.left.compute_height(), self.right.compute_height()) + 1

    def rotate_right(self):
        left = self.left
        right_of_left = left.right

        _set_child_of_parent(self, left)
        self.left = right_of_left
        left.right = self
    
    def rotate_left(self):
        right = self.right # right was promoted
        left_of_right = right.left

        _set_child_of_parent(self, right)
        self.right = left_of_right # TODO: was left of right promoted?
        right.left = self

"""Sets the child to refer to a different node, i.e. (parent = `child.parent`) if parent.x (where x is 'left' or 'right') is `child`, parent.x will be set to `node`"""
def _set_child_of_parent(child: AVLNode, node: (AVLNode | None)):
    parent = child.parent
    
    if parent is None:
        return
    
    if parent.left is child:
        parent.left = node
    else:
        parent.right = node


"""
A class implementing an AVL tree.
"""
class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """
    def __init__(self, root: (AVLNode | None) = None):
        self.root = root
        self._max = None

        if self.root is not None:
            assert not self.root.left.is_real_node and not self.root.right.is_real_node and self.root.parent is None
            self._max = self.root

    """searches for a node in the dictionary corresponding to the key (starting at the root)
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def search(self, key: int) -> Tuple[AVLNode, int]:
        x, e, found = AVLTree._search_core(self.root, key, 1)
        if not found:
            x = None
        return x, e

    """
    @returns: a tuple (x, e, found) where x is the node if found, else last node checked
    """
    @staticmethod
    def _search_core(node: AVLNode, key: int, e: int) -> Tuple[(AVLNode | None), int, bool]:
        if not _is_real(node):
            return node.parent if node is not None else None, e, False # node is None iff self.root is None

        if key == node.key:
            return node, e, True

        if key < node.key:
            return AVLTree._search_core(node.left, key, e + 1)

        return AVLTree._search_core(node.right, key, e + 1)

    """searches for a node in the dictionary corresponding to the key, starting at the max
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def finger_search(self, key: int) -> Tuple[AVLNode, int]:
        x, e, found = AVLTree._finger_search_core(self.max_node(), key, 1)
        if not found:
            x = None
        return x, e

    @staticmethod
    def _finger_search_core(node: AVLNode, key: int, e: int) -> Tuple[(AVLNode | None), int, bool]:
        if not _is_real(node): # iff self.max_node() is None iff self.root is None
            assert node is None
            return None, e, False

        if key == node.key:
            return node, e, True
        
        if node.parent is None or key > node.parent.key:
            return AVLTree._search_core(node.left, key, e + 1)
        
        return AVLTree._finger_search_core(node.parent, key, e + 1)

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
        parent, e, found = AVLTree._search_core(self.root, key, 1)
        return self._insert_core(key, val, parent, e, found)

    def _insert_core(self, key: int, val: str, parent: (AVLNode | None), e: int, found: bool) -> Tuple[AVLNode, int, int]:
        if found:
            parent.value = val
            return parent, e, 0

        new_node = AVLNode(key, val)

        if parent is None: # no root
            assert self.root is None
            self.root = new_node
            self._max = new_node
            return new_node, e, 0

        if key < parent.key:
            assert not _is_real(parent.left)
            parent.left = new_node
        else:
            assert not _is_real(parent.right)
            parent.right = new_node
        
        h = self.rebalance(new_node)
        
        if new_node.key > self._max.key:
            self._max = new_node

        return new_node, e, h

    # Balances the first subtree up from the passed node
    def rebalance(self, node: AVLNode) -> int:
        if node.left.is_real_node or node.right.is_real_node:
            raise ValueError('Parameter "node" must be a leaf.')

        child = node
        node = node.parent
        while node is not None:
            if abs(node.balance_factor) > 1:
                break
            child = node
            node = node.parent

        if node is None:
            return

        h = -1
        if node.balance_factor > 0:
            if child.balance_factor > 0: # LL imbalance
                assert node.balance_factor > 1 and node.left.is_real_node and node.left.balance_factor > 0
                node.rotate_right()
                h = 1
            else: # LR imbalance
                assert node.balance_factor > 1 and node.left.is_real_node and node.left.balance_factor < 0 and node.left.right.is_real_node
                node.left.rotate_left()
                node.rotate_right()
                h = 2
        else:
            if child.balance_factor > 0: # RL imbalance
                assert node.balance_factor < -1 and node.right.is_real_node and node.right.balance_factor > 0 and node.right.left.is_real_node
                node.right.rotate_right()
                node.rotate_left()
                h = 2
            else: # RR imbalance
                assert node.balance_factor < -1 and node.right.is_real_node and node.right.balance_factor < 0
                node.rotate_left()
                h = 1
        
        if self.root is node:
            self.root = node.parent
        return h

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
        parent, e, found = AVLTree._finger_search_core(self.max_node(), key, 1)
        return self._insert_core(key, val, parent, e, found)

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
        def _insert_nodes(node: AVLNode, tree: Self):
            if not _is_real(node):
                return

            _insert_nodes(node.left, tree)
            tree.insert(node)
            _insert_nodes(node.right, tree)
        
        self.insert(AVLNode(key, val))
        _insert_nodes(tree2.get_root(), self)

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
        def _avl_to_array(node: AVLNode, list: list):
            if not _is_real(node):
                return

            _avl_to_array(node.left, list)
            list.append((node.key, node.value))
            _avl_to_array(node.right, list)
        
        lst = []
        _avl_to_array(self.root, lst)
        return lst

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """
    def max_node(self) -> AVLNode:
        node = self.root
        while _is_real(node):
            node = node.right
        assert node is self._max
        return self._max

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    def size(self) -> int:
        def _size(node):
            if not _is_real(node):
                return 0
            
            return _size(node.left) + _size(node.right) + 1

        return _size(self.root)

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self) -> AVLNode:
        return self.root

def _is_real(node: (AVLNode | None)):
    return node is not None and node.is_real_node
