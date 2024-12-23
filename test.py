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

def get_nodes_with_no_parent(root):
    def rec(node: AVLNode, list: list):
        if not _is_real(node):
            return

        rec(node.left, list)
        if node.parent is None:
            list.append(node)
        rec(node.right, list)
    
    lst = []
    rec(root, lst)
    return lst

# root = AVLNode(40, '40')
# root.right = AVLNode(45, '45')
# root.left = AVLNode(30, '30')
# root.left.left = AVLNode(20, '20')
# root.right.left = AVLNode(44, '44')

tree = AVLTree(AVLNode(50, ''))
tree.insert(40, '')
tree.insert(45, '')
tree.insert(30, '')
tree.insert(20, '')
tree.insert(60, '')
tree.insert(55, '')
tree.insert(70, '')
tree.insert(65, '')
tree.insert(80, '')
tree.insert(90, '')

pt(tree.root)
