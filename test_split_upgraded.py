from AVLTree import *
import random

def predecessor(node):
    x=node
    if x is None:
        return None
    if node.left.is_real_node():
        x=node.left
        while x.right.is_real_node():
            x=x.right
        return x
    while x.parent is not None:
        if x.parent.right == x:
            return x.parent
        x=x.parent
    return None


def in_order_list(t):
    keys = []
    if t.root is None:
        return keys
    in_order_rec(t.root, keys)
    return keys

def in_order_rec(node, keys):
    if node.key is not None:
        in_order_rec(node.left, keys)
        h=max(node.left.height, node.right.height) + 1
        assert node.height==h, f"height of node: {node.key} is wrong. it's {node.height} instead of {h}"
        assert abs(node.left.height-node.right.height) <2, f"balance factor of node: {node.key} is too big - it is not an AVL tree!"
        if node.left.is_real_node():
            assert node.left.parent is node, f"problem with left child of node: {node.key}"
        if node.right.is_real_node():
            assert node.right.parent is node, f"problem with right child of node: {node.key}"
        keys.append(node.key)
        in_order_rec(node.right, keys)


def split_test(TREE_SIZE):
    t=AVLTree()
    rand_list = random.sample(range(10*TREE_SIZE), TREE_SIZE)
    for item in rand_list:
        t.insert(key=item,val="d")
    ind=random.randint(0, TREE_SIZE-1)
    split_key=rand_list[ind]
    split_node=t.search(split_key)[0]
    max1=predecessor(split_node)
    t1,t2=t.split(split_node)
    if t1.root is not None:
        assert t1.root.parent is None, "problem with the parent of the root of the tree with the smaller keys - it is not None"
    if t2.root is not None:
        assert t2.root.parent is None, "problem with the parent of the root of the tree with the greater keys - it is not None"
    max2=t2.max_node()
    keys1=in_order_list(t1)
    keys2=in_order_list(t2)
    assert len(keys1)+len(keys2)+1==TREE_SIZE, "some nodes got lost or were accidentally added during splitting"
    assert keys1==sorted(keys1), "the tree with the smaller nodes is not a search tree"
    assert keys2==sorted(keys2), "the tree with the greater nodes is not a search tree"
    for i in range(len(keys1)):
        assert keys1[i]<split_key, "the tree with the smaller nodes is wrong"
    for i in range(len(keys2)):
        assert keys2[i]>split_key, "the tree with the greater nodes is wrong"
    str1= "max_node of the tree with the smaller keys is wrong"
    if max1 is None:
        assert t1.max_node() is None, str1
    elif t1.max_node() is None:
        assert max1 is None, str1
    else:
        assert max1.key==t1.max_node().key, str1
    str2="max_node of the tree with the greater keys is wrong"
    if max2 is None:
        assert t2.max_node() is None, str2
    elif t2.max_node() is None:
        assert max2 is None, str2
    else:
        assert max2.key==t2.max_node().key, str2

NUM_OF_TESTS =15
MAX_SIZE=20
for i in range(1,MAX_SIZE+1):
    for j in range(NUM_OF_TESTS):
        split_test(TREE_SIZE = i)