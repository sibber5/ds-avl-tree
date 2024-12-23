# id1: 213856032
# name1: Nara Zangariya
# username1: naraz
# id2: 213513443
# name2: Ghassan Jadoun
# username2: ghassanj

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

    def ll_rotate(self):
        valid = self.balance_factor == 2 \
                and self.left.is_real_node and not self.right.is_real_node \
                and self.left.left.is_real_node and not self.left.right.is_real_node \
                and self.left.left.height == 0
        if not valid:
            raise ValueError()

    def lr_rotate(self):
        valid = self.balance_factor == 2 \
                and self.left.is_real_node and not self.right.is_real_node \
                and not self.left.left.is_real_node and self.left.right.is_real_node \
                and self.left.right.height == 0
        if not valid:
            raise ValueError()

    def rl_rotate(self):
        valid = self.balance_factor == -2 \
                and not self.left.is_real_node and self.right.is_real_node \
                and self.right.left.is_real_node and not self.right.right.is_real_node \
                and self.right.left.height == 0
        if not valid:
            raise ValueError()

    def rr_rotate(self):
        valid = self.balance_factor == -2 \
                and not self.left.is_real_node and self.right.is_real_node \
                and not self.right.left.is_real_node and self.right.right.is_real_node \
                and self.right.right.height == 0
        if not valid:
            raise ValueError()

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

    def __init__(self, root: (AVLNode | None) = None):
        self.root = root

    # TODO: balance root if unbalanced

    """searches for a node in the dictionary corresponding to the key (starting at the root)
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def search(self, key: int) -> Tuple[AVLNode, int]:
        (x, e, found) = AVLTree._search_rec(None, self.root, 1, key)
        if not found:
            x = None
        return x, e

    """
    @returns: a tuple (x, e, found) where x is the node if found, else last node checked
    """

    @staticmethod
    def _search_rec(parent: (AVLNode | None), node: AVLNode, e: int, key: int) -> Tuple[AVLNode, int, bool]:
        if not AVLTree._is_real_node(node):
            return parent, e, False

        if node.key == key:
            return node, e, True

        if node.key > key:
            return AVLTree._search_rec(node, node.left, e + 1, key)

        return AVLTree._search_rec(node, node.right, e + 1, key)

    """searches for a node in the dictionary corresponding to the key, starting at the max
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def finger_search(self, key: int) -> Tuple[AVLNode, int]:
        return AVLTree._search_from_max(self.max_node(), key, 0)

    @staticmethod
    def _search_from_max(self, node, key, depth):
        if node is None:
            return None, depth

        if key == node.key:
            return node, depth
        if node.parent is not None:
            if node.key > key > node.parent.key:
                return self._search_from_max(node.left, key, depth + 1)
            if node.key < key < node.parent.key:
                return self._search_from_max(node.right, key, depth + 1)
        if node.parent is None:
            self._search_from_max(node.left, key, depth + 1)
        return self._search_from_max(node.parent, key, depth + 1)

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
        parent, e, found = AVLTree._search_rec(None, self.root, 1, key)

        if found:
            parent.value = val
            return parent, e, 0

        new_node = AVLNode(key, val)
        h = 0

        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self.balance(new_node)
        return new_node, e, h

    # Balances from the parent node up
    def balance(self, node: AVLNode):
        if node.left.is_real_node or node.right.is_real_node:
            raise ValueError("node must be leaf")

        child = node
        node = node.parent
        while node is not None:
            if abs(node.balance_factor) > 1:
                break
            child = node
            node = node.parent

        if node.balance_factor > 0:
            if child.balance_factor > 0:
                node.ll_rotate()
            else:
                node.lr_rotate()
        else:
            if child.balance_factor > 0:
                node.rl_rotate()
            else:
                node.rr_rotate()

    def rotate_right(self, n):
        newleftforparent = n.getRight()
        parent = n.getParent()
        if (parent is not None):
            n.setParent(parent.getParent())
        if (n.getParent() != None):
            if (n.getParent().getLeft() == parent):
                n.getParent().setLeft(n)
            if (n.getParent().getRight() == parent):
                n.getParent().setRight(n)
        n.setRight(parent)
        parent.setParent(n)
        parent.setLeft(newleftforparent)
        newleftforparent.setParent(parent)
        parent.setHeight(max(parent.getRight().getHeight(), parent.getLeft().getHeight()) + 1)
        parent.setSize(parent.getRight().getSize() + parent.getLeft().getSize() + 1)
        n.setSize(n.getRight().getSize() + n.getLeft().getSize() + 1)
        n.setHeight(max(n.getRight().getHeight(), n.getLeft().getHeight()) + 1)

    def rotate_left(self, n):
        newrightforparent = n.getLeft()
        parent = n.getParent()
        if (parent is not None):
            n.setParent(parent.getParent())
        if (n.getParent() != None):
            if (n.getParent().getLeft() == parent):
                n.getParent().setLeft(n)
            if (n.getParent().getRight() == parent):
                n.getParent().setRight(n)
        n.setLeft(parent)
        parent.setParent(n)
        parent.setRight(newrightforparent)
        newrightforparent.setParent(parent)
        parent.setHeight(max(parent.getRight().getHeight(), parent.getLeft().getHeight()) + 1)
        parent.setSize(parent.getRight().getSize() + parent.getLeft().getSize() + 1)
        n.setSize(n.getRight().getSize() + n.getLeft().getSize() + 1)
        n.setHeight(max(n.getRight().getHeight(), n.getLeft().getHeight()) + 1)

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
        list = []
        AVLTree._avl_to_array_rec(self.root, list)
        return list

    @staticmethod
    def _avl_to_array_rec(node: AVLNode, list: list):
        if not AVLTree._is_real_node(node):
            return

        AVLTree._avl_to_array_rec(node.left, list)
        list.append(node.value)
        AVLTree._avl_to_array_rec(node.right, list)

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """

    def max_node(self) -> AVLNode:
        node = self.root
        while AVLTree._is_real_node(node):
            node = node.right
        return node

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self) -> int:
        return self._size(self.root)

    def _size(self, node):
        if not AVLTree._is_real_node(node):
            return 0
        left_size = self._size(node.left)
        right_size = self._size(node.right)
        return 1 + left_size + right_size

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self) -> AVLNode:
        return self.root

    @staticmethod
    def _is_real_node(node: (AVLNode | None)):
        return node is not None and node.is_real_node
