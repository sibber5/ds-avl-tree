import random

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

# tree = AVLTree()
# for i in [5, 27, 29, 37, 1, 50, 36, 66]:
# for i in [8, 4, 15, 3, 6, 11, 54]:
    # tree.insert(i, '')
# x, _ = tree.search(66)

# print(tree.max_node())
# print()
# pt(tree.root)
# print(tree.finger_search(11))
# print(tree.finger_search(32))

# tree.delete(tree.root.left.left)
# tree.delete_node(tree.root, tree.root.left.left.key)
# delete_node(tree, 15)
# t1, t2 = tree.split(x)

# print()
# print("t1:")
# _ = pt(t1.root) if t1.root is not None else None
# print("t2:")
# _ = pt(t2.root) if t2.root is not None else None

def get_arrays(k):
    n = 111 * (2**k)
    # n = k
    sorted_arr = list(range(1, n + 1))
    reverse_arr = list(reversed(sorted_arr))
    shuffled_arr = list(sorted_arr)
    random.shuffle(shuffled_arr)
    index_swap_arr = list(sorted_arr)
    for j in range(len(index_swap_arr) - 1):
        if random.random() > 0.5:
            index_swap_arr[j], index_swap_arr[j + 1] = index_swap_arr[j + 1], index_swap_arr[j]
    return sorted_arr, reverse_arr, shuffled_arr, index_swap_arr

def get_promote_count(arr):
    tree = AVLTree()
    count = 0
    for item in arr:
        _, _, h = tree.finger_insert(item, '')
        count += h
    return count

def get_paths_count(arr):
    tree = AVLTree()
    count = 0
    for item in arr:
        _, e, _ = tree.finger_insert(item, '')
        count += e
    return count

def get_average(i, get_count):
    shuffled_count_0 = 0
    swapped_count_0 = 0
    for j in range(20):
        _, _, shuffled, index_swap = get_arrays(i)
        shuffled_count_0 += get_count(shuffled)
        swapped_count_0 += get_count(index_swap)
    return shuffled_count_0 / 20, swapped_count_0 / 20

def get_reverse_count(arr):
    reverses = 0
    for j in range(len(arr)):
        for k in range(j):
            if arr[k] > arr[j]:
                reverses += 1
    return reverses

print("i, sorted, reversed, shuffled, swapped")
get_count = get_paths_count
for i in range(1, 11):
    sorted_0, reversed_0, _, _ = get_arrays(i)
    sorted_count = get_count(sorted_0)
    reversed_count = get_count(reversed_0)
    shuffled_count, swapped_count = get_average(i, get_count)
    print(f"{i}, {sorted_count}, {reversed_count}, {shuffled_count}, {swapped_count}")

# tree = AVLTree()
# _, _, h = tree.insert(3, '')
# print(h)
# _, _, h = tree.insert(1, '')
# print(h)
# _, _, h = tree.insert(2, '')
# print(h)
