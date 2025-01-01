from AVLTree import *
from PrettyPrint import PrettyPrintTree

def get_children(node: AVLNode):
    lst = []
    if node.left.is_real_node():
        lst.append(node.left)
    if node.right.is_real_node():
        lst.append(node.right)
    return lst
pt = PrettyPrintTree(get_children, lambda x: x.key)

# root = AVLNode(40, '40')
# root.right = AVLNode(45, '45')
# root.left = AVLNode(30, '30')
# root.left.left = AVLNode(20, '20')
# root.right.left = AVLNode(44, '44')

tree = AVLTree()
tree.insert(5234, '')
tree.max_node()
tree.finger_insert(7547, '')
tree.max_node()
tree.insert(4665, '')
tree.max_node()
tree.finger_insert(8108, '')
tree.max_node()
tree.delete(tree.search(1640)[0])
tree.max_node()
tree.finger_insert(6352, '')
tree.max_node()
tree.delete(tree.search(8108)[0])
tree.max_node()
tree.insert(6845, '')
tree.max_node()
tree.insert(3524, '')
tree.max_node()
tree.finger_insert(8319, '')
# for i in [5, 27, 29, 37, 1, 50, 36, 66]:
# for i in [20, 55, 60, 75, 35, 40, 15, 90, 80, 25, 62, 65]:
#     tree.insert(i, '')
# x, _ = tree.search(66)

print(tree.max_node())
print()
pt(tree.root)

# tree.delete(tree.root.left.left)
# tree.delete_node(tree.root, tree.root.left.left.key)
# delete_node(tree, 15)
# t1, t2 = tree.split(x)

# print()
# print("t1:")
# _ = pt(t1.root) if t1.root is not None else None
# print("t2:")
# _ = pt(t2.root) if t2.root is not None else None
