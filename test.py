from AVLTree import *
from PrettyPrint import PrettyPrintTree

def get_children(node: AVLNode):
    lst = []
    if node.left.is_real_node:
        lst.append(node.left)
    if node.right.is_real_node:
        lst.append(node.right)
    return lst
pt = PrettyPrintTree(get_children, lambda x: x.key)

# root = AVLNode(40, '40')
# root.right = AVLNode(45, '45')
# root.left = AVLNode(30, '30')
# root.left.left = AVLNode(20, '20')
# root.right.left = AVLNode(44, '44')

tree = AVLTree(AVLNode(50, ''))
tree.insert(25, '')
tree.insert(75, '')
tree.insert(15, '')
tree.insert(40, '')
tree.insert(60, '')
tree.insert(80, '')
tree.insert(35, '')
tree.insert(55, '')
tree.insert(65, '')
tree.insert(90, '')
tree.insert(62, '')

pt(tree.root)

tree.delete(tree.root.left.left)
# tree.delete_node(tree.root, tree.root.left.left.key)
# delete_node(tree, 15)

print()
pt(tree.root)
