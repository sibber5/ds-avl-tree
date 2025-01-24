#id1: 214611055
#name1: Majd Shhadi
#username1: Majdishhadi
#id2: 213513443
#name2: Ghassan Jadoun
#username2: ghassanj

from typing import Self, Tuple

"""A class represnting a node in an AVL tree"""
class AVLNode(object):
    _auto_update_heights: bool = True

    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node. creates virtual node if None is passed.
    @type value: string
    @param value: data of your node
    """
    def __init__(self, key: int, value: str):
        if key is None:
            self.key = None
            self._parent: AVLNode = None
            self._height = -1
        else:
            self.key = key
            self.value = value
            self._left = AVLNode.virtual()
            self._left._parent = self
            self._right = AVLNode.virtual()
            self._right._parent = self
            self._parent: AVLNode = None
            self._height = 0

    @classmethod
    def virtual(cls):
        return cls(None, None)

    @property
    def left(self) -> Self:
        if not self.is_real_node():
            return None
        # self._raise_if_virtual_node()
        return self._left

    """
    Time complexity: 
    If _auto_update_heights = True, O(log n) (where n is the number of nodes in the tree) because it will update the heights of all nodes above it up to the root, 
    so at most height(tree) operations and for an avl tree height(tree) = O(log n). 
    If _auto_update_heights = False, O(1)
    """
    @left.setter
    def left(self, val: (Self | None)):
        self._raise_if_virtual_node()
        if val is None:
            val = AVLNode.virtual()

        self._left._parent = None
        self._left = val
        _set_child_of_parent(val, None)
        val._parent = self
        if AVLNode._auto_update_heights:
            self._update_heights_up()
        assert (not self._left.is_real_node()) or self._left.key < self.key

    @property
    def right(self) -> Self:
        if not self.is_real_node():
            return None
        # self._raise_if_virtual_node()
        return self._right
    
    """
    Time complexity: 
    If _auto_update_heights = True, O(log n) (where n is the number of nodes in the tree) because it will update the heights of all nodes above it up to the root, 
    so at most height(tree) operations and for an avl tree height(tree) = O(log n). 
    If _auto_update_heights = False, O(1)
    """
    @right.setter
    def right(self, val: (Self | None)):
        self._raise_if_virtual_node()
        if val is None:
            val = AVLNode.virtual()

        self._right._parent = None
        self._right = val
        _set_child_of_parent(val, None)
        val._parent = self
        if AVLNode._auto_update_heights:
            self._update_heights_up()
        assert (not self._right.is_real_node()) or self._right.key > self.key

    @property
    def parent(self):
        return self._parent

    @property
    def height(self):
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
    def is_real_node(self):
        return self.key is not None

    def _raise_if_virtual_node(self):
        if not self.is_real_node():
            raise RuntimeError('Invalid operation on virtual node.')

    def _update_height(self):
        self._height = max(self.left.height, self.right.height) + 1

    """
    Time complexity: O(log n) (where n is the number of nodes in the tree) because it will update the heights of all nodes above it up to the root, 
    so at most height(tree) operations and for an avl tree height(tree) = O(log n).
    """
    def _update_heights_up(self):
        h = 0
        while self is not None:
            new_height = max(self.left.height, self.right.height) + 1
            if new_height > self._height:
                h += 1
            elif new_height == self._height and AVLNode._auto_update_heights:
                break
            self._height = new_height
            self = self.parent
        return h

    """
    Time complexity: 
    If _auto_update_heights = False, O(log n) (where n is the number of nodes in the tree) because it will update the heights of all nodes above it up to the root, 
    so at most height(tree) operations and for an avl tree height(tree) = O(log n). 
    If _auto_update_heights = True, O(1)
    """
    def rotate_right(self):
        left = self.left
        right_of_left = left.right

        _set_child_of_parent(self, left)
        self.left = right_of_left
        left.right = self

        # when inserting _auto_update_heights would be False because we want to count the promote cases. but there are no promote
        # cases when rotating, so we auto update the heights of the rotated nodes despite auto updating being off to make the code simpler.
        if AVLNode._auto_update_heights == False:
            self._update_height()
            self.parent._update_height()
    
    """
    Time complexity: 
    If _auto_update_heights = False, O(log n) (where n is the number of nodes in the tree) because it will update the heights of all nodes above it up to the root, 
    so at most height(tree) operations and for an avl tree height(tree) = O(log n). 
    If _auto_update_heights = True, O(1)
    """
    def rotate_left(self):
        right = self.right
        left_of_right = right.left

        _set_child_of_parent(self, right)
        self.right = left_of_right
        right.left = self

        if AVLNode._auto_update_heights == False:
            self._update_height()
            self.parent._update_height()

"""Sets the child to refer to a different node, i.e. (parent = `child.parent`) if parent.x (where x is 'left' or 'right') is `child`, parent.x will be set to `node`"""
def _set_child_of_parent(child: AVLNode, node: (AVLNode | None)):
    parent = child.parent
    
    if parent is None:
        if node is not None:
            _set_child_of_parent(node, None)
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
            if self.root.left.is_real_node() or self.root.right.is_real_node() or self.root.parent is not None:
                raise ValueError("root must not have child nodes nor parent.")
            self._max = self.root

    """
    searches for a node in the dictionary corresponding to the key (starting at the root)
    
    Time complexity: (from _search_core which is what does the work) O(log n) (where n is the number of nodes in the tree), because worst case it will traverse to the leaf with the highest depth, 
    which is equal to the height of the root aka the height of the tree which is log n for an avl tree.

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
    Time complexity: O(log n) (where n is the number of nodes in the tree), because worst case it will traverse to the leaf with the highest depth, 
    which is equal to the height of the root aka the height of the tree which is log n for an avl tree.

    @returns: a tuple (x, e, found) where x is the node if found, else last node checked
    """
    @staticmethod
    def _search_core(node: AVLNode, key: int, e: int) -> Tuple[(AVLNode | None), int, bool]:
        if node is None: # iff self.root is None
            return None, e, False
        if not node.is_real_node():
            return node.parent, e - 1, False

        if key == node.key:
            return node, e, True

        if key < node.key:
            return AVLTree._search_core(node.left, key, e + 1)

        return AVLTree._search_core(node.right, key, e + 1)

    """
    searches for a node in the dictionary corresponding to the key, starting at the max
    
    Time complexity: (from _finger_search_core which is what does the work) O(log n) (where n is the number of nodes in the tree), because worst case it will traverse up from the max to the root and down to a leaf with the highest depth, 
    which is at most 2height(tree) and for an avl tree height(tree) = log n so time complexity is O(2log n) = O(log n).

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

    """
    Time complexity: O(log n) (where n is the number of nodes in the tree), because worst case it will traverse up from the max to the root and down to a leaf with the highest depth, 
    which is at most 2height(tree) and for an avl tree height(tree) = log n so time complexity is O(2log n) = O(log n).
    """
    @staticmethod
    def _finger_search_core(node: AVLNode, key: int, e: int) -> Tuple[(AVLNode | None), int, bool]:
        if not _is_real(node): # iff self.max_node() is None iff self.root is None
            assert node is None
            return None, e, False

        if key > node.key: # iff key > max_node.key
            assert e == 1
            return node, e, False

        if key == node.key:
            return node, e, True
        
        if node.parent is None or key > node.parent.key:
            return AVLTree._search_core(node.left, key, e + 1)
        
        return AVLTree._finger_search_core(node.parent, key, e + 1)

    """
    inserts a new node into the dictionary with corresponding key and value (starting at the root)

    Time complexity: O(log n) = Complexity(_search_core) + Complexity(_insert_core) = O(log n) + O(log n)

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

    """
    Time complexity: O(log n) = Complexity(_update_heights_and_rebalance) because everything is O(1) except for _update_heights_and_rebalance (setting node.left or node.right is O(1) since AVLNode._auto_update_heights = False)
    """
    def _insert_core(self, key: int, val: str, parent: (AVLNode | None), e: int, found: bool) -> Tuple[AVLNode, int, int]:
        if found:
            parent.value = val
            return parent, e, 0

        new_node = AVLNode(key, val)

        if parent is None: # no root
            assert self.root is None
            self.root = new_node
            self._max = new_node
            return new_node, e - 1, 0

        AVLNode._auto_update_heights = False
        prev_bf = parent.balance_factor

        if key < parent.key:
            assert not _is_real(parent.left)
            parent.left = new_node
        else:
            assert not _is_real(parent.right)
            parent.right = new_node
        
        h = self._update_heights_and_rebalance(new_node, prev_bf)
        AVLNode._auto_update_heights = True

        if new_node.key > self._max.key:
            self._max = new_node

        return new_node, e, h

    """
    Time complexity: O(log n), Complexity(_rebalance) = O(1) since AVLNode._auto_update_heights = False, so worst we traverse up to the root in order to update the heights and/or do rotations which are O(1) as stated earlier,
    and traversing up to the root is O(height(tree)) = O(log n).
    """
    def _update_heights_and_rebalance(self, node: (AVLNode | None), prev_bf: int):
        assert AVLNode._auto_update_heights == False

        h = 0
        while node is not None:
            assert node._height == max(node.left.height, node.right.height) + 1

            if node.parent is None:
                return h
            
            if prev_bf == 0: # case 1
                prev_bf = node.parent.parent.balance_factor if node.parent.parent is not None else None
                node.parent._height += 1
                h += 1
                node = node.parent
                continue
            
            if abs(prev_bf) == 1:
                if node.parent.balance_factor == 0:
                    return h
                
                # case 2 + 3
                assert abs(node.parent.balance_factor) == 2
                self._rebalance(node.parent)
                return h

            raise ValueError(f'Invalid balance factor: {prev_bf}.')
        return h
        

    """
    inserts a new node into the dictionary with corresponding key and value, starting at the max

    Time complexity: O(log n) = Complexity(_finger_search_core) + Complexity(_insert_core) = O(log n) + O(log n)

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

    """
    deletes node from the dictionary

    Time complexitY: O(log n), calculating max is O(log n) and deleting the node itself is O(log n) worst case in case we need to update all the heights
    (which is done when setting a child node, as explaned in the property setters in AVLNode), and rebalancing is O(log n) worst case in case we need to rebalance all the way up to the root
    (rotations themselves are O(1)). So O(3log n) = O(log n)

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def delete(self, node: AVLNode):
        if node.left.is_real_node() and node.right.is_real_node():
            max_left = _get_max(node.left)
            _swap_nodes(node, max_left)
            if self.root is node:
                self.root = max_left
            self.delete(node)
            return
        
        temp = node.left if node.left.is_real_node() else node.right
        if not temp.is_real_node(): # if node is a leaf
            temp = node.parent
            if self.root is node:
                self.root = None
            _set_child_of_parent(node, None)
        else: # if node has 1 child
            if self.root is node:
                self.root = temp
                _set_child_of_parent(temp, None)
            else:
                _set_child_of_parent(node, temp)

        self._rebalance_up_from(temp)

        self._max = _get_max(self.root)

    """joins self with item and another AVLTree

    Time complexity: O(log n) as proved in the lecture.

    @type tree2: AVLTree 
    @param tree2: a dictionary to be joined with self
    @type key: int 
    @param key: the key separting self and tree2
    @type val: string
    @param val: the value corresponding to key
    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
    or the opposite way
    """
    def join(self, tree2: (Self | None), key: int, val: str):
        self._join_core(tree2.root if tree2 is not None else None, AVLNode(key, val))
    
    def _join_core(self, tree2_root: (AVLNode | None), median: AVLNode):
        assert median is not None and (median.is_real_node() and not median.left.is_real_node() and not median.right.is_real_node() and median.parent is None)
        assert tree2_root is None or tree2_root.parent is None

        if not _is_real(tree2_root):
            self.insert(median.key, median.value)
            return

        if not _is_real(self.root):
            self.root = tree2_root
            self._max = _get_max(self.root)
            self.insert(median.key, median.value)
            return

        x = median

        smaller = self.root
        larger = tree2_root
        if smaller.key > larger.key:
            smaller, larger = larger, smaller

        if smaller.height <= larger.height:
            b = larger
            while b.height > smaller.height and _is_real(b.left):
                b = b.left
            
            c = b.parent
            
            x.left = smaller
            x.right = b
            if _is_real(c):
                c.left = x
                self.root = larger
            else:
                assert x.parent is None and larger is b
                self.root = x
        else:
            b = smaller
            while b.height > larger.height and _is_real(b.right):
                b = b.right
            
            c = b.parent
            
            x.left = b
            x.right = larger
            if _is_real(c):
                c.right = x
                self.root = smaller
            else:
                assert x.parent is None and smaller is b
                self.root = x

        self._rebalance_up_from(x)

        self._max = _get_max(self.root)

    """splits the dictionary at a given node

    Time complexity: O(log n) as proved in the lecture.

    @type node: AVLNode
    @pre: node is in self
    @param node: the node in the dictionary to be used for the split
    @rtype: (AVLTree, AVLTree)
    @returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """
    def split(self, node: AVLNode) -> Tuple[Self, Self]:
        smaller = AVLTree()
        larger = AVLTree()

        up_left = None
        while _is_real(node):
            left = node.left
            right = node.right
            parent = node.parent
            going_up_left = node is parent.right if _is_real(parent) else None

            _set_child_of_parent(node, None)
            node.left = None
            node.right = None

            if up_left is None:
                if left.is_real_node():
                    smaller.root = left
                    smaller._max = _get_max(left)
                if right.is_real_node():
                    larger.root = right
                    larger._max = _get_max(right)
            elif up_left:
                smaller._join_core(left, node)
            else:
                larger._join_core(right, node)
            
            up_left = going_up_left
            node = parent

        assert smaller._max is _get_max(smaller.root)
        assert larger._max is _get_max(larger.root)
        return smaller, larger

    """
    returns an array representing dictionary

    Time complexity: O(n) since we need to iterate over all of the nodes in order to add them to the list.
    
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
    def max_node(self) -> (AVLNode | None):
        # assert _get_max(self.root) is self._max # TODO: remove before submitting
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

    """
    Time complexity: O(1) if AVLNode._auto_update_heights = False, otherwise O(log n) in case we need to update the heights all the way up to the root.
    """
    def _rebalance(self, node: AVLNode):
        assert _is_real(node)

        if abs(node.balance_factor) < 2:
            return

        if node.balance_factor > 0:
            if node.left.balance_factor >= 0: # LL imbalance
                assert node.balance_factor > 1 and node.left.is_real_node() and node.left.balance_factor >= 0
                node.rotate_right()
            else: # LR imbalance
                assert node.balance_factor > 1 and node.left.is_real_node() and node.left.balance_factor < 0 and node.left.right.is_real_node()
                node.left.rotate_left()
                node.rotate_right()
        else:
            if node.right.balance_factor <= 0: # RR imbalance
                assert node.balance_factor < -1 and node.right.is_real_node() and node.right.balance_factor <= 0
                node.rotate_left()
            else: # RL imbalance
                assert node.balance_factor < -1 and node.right.is_real_node() and node.right.balance_factor > 0 and node.right.left.is_real_node()
                node.right.rotate_right()
                node.rotate_left()

        if self.root is node:
            self.root = node.parent
            assert self.root.parent is None

        return

    """
    Time complexity: O(log n) in case we need to rebalance all the way to the root.
    """
    def _rebalance_up_from(self, node: AVLNode):
        while node is not None:
            self._rebalance(node)
            node = node.parent


def _is_real(node: (AVLNode | None)):
    return node is not None and node.is_real_node()

"""
O(log n) because worst case the max node has the highest depth which is height(tree) = log n
"""
def _get_max(node: AVLNode) -> (AVLNode | None):
    if _is_real(node):
        while _is_real(node.right):
            node = node.right
        return node
    else:
        return None

def _swap_nodes(old: AVLNode, new: AVLNode):
    def swap_parent_child(parent: AVLNode, child: AVLNode):
        child_left = child._left
        child_right = child._right
        child_height = child._height

        child._parent = parent._parent
        child._height = parent._height
        parent._height = child_height
        parent._parent = child

        if parent._left is child:
            child._right = parent._right
            parent._right._parent = child
            child._left = parent
        else:
            child._right = parent
            child._left = parent._left
            parent._left._parent = child
        
        parent._left = child_left
        child_left._parent = parent
        parent._right = child_right
        child_right._parent = parent

        if child._parent is None:
            return
        if child._parent._left is parent:
            child._parent._left = child
        else:
            child._parent._right = child

    if new._parent is old:
        swap_parent_child(old, new)
        return
    elif old._parent is new:
        swap_parent_child(new, old)
        return

    new_left = new._left
    new_right = new._right
    new_parent = new._parent
    new_height = new._height

    new._left = old._left
    new._left._parent = new
    new._right = old._right
    new._right._parent = new
    new._parent = old._parent
    new._height = old._height

    if old._parent is not None:
        if old._parent._left is old:
            old._parent._left = new
        else:
            old._parent._right = new

    old._left = new_left
    old._left._parent = old
    old._right = new_right
    old._right._parent = old
    old._parent = new_parent
    old._height = new_height

    if new_parent is not None:
        if new_parent._left is new:
            new_parent._left = old
        else:
            new_parent._right = old
