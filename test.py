from avl_tree import AVLTree
from printree import printree

if __name__ == "__main__":
    tree = AVLTree()
    # First batch of insertions
    for key in [30, 20, 10, 25, 35, 40, 103, 108, 305]:
        tree.insert(key, str(key))
    print('After first insertions:')
    printree(tree.root)
    with open('tree_output.txt', 'w') as f:
        printree(tree.root, file=f)

    # First batch of removals
    for key in [20, 40]:
        node = tree.search(key)
        if node:
            tree.delete(node)
    print('\nAfter first removals:')
    printree(tree.root)
    with open('tree_output.txt', 'a') as f:
        print('\nAfter first removals:', file=f)
        printree(tree.root, file=f)

    # Second batch of insertions
    for key in [50, 60, 70]:
        tree.insert(key, str(key))
    print('\nAfter second insertions:')
    printree(tree.root)
    with open('tree_output.txt', 'a') as f:
        print('\nAfter second insertions:', file=f)
        printree(tree.root, file=f)

    # Second batch of removals
    for key in [10, 305]:
        node = tree.search(key)
        if node:
            tree.delete(node)
    print('\nAfter second removals:')
    printree(tree.root)
    with open('tree_output.txt', 'a') as f:
        print('\nAfter second removals:', file=f)
        printree(tree.root, file=f)