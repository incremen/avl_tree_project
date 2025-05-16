from avl_tree import AVLTree
from printree import printree

if __name__ == "__main__":
    tree = AVLTree()
    for key in [30, 20, 10, 25, 35]:
        tree.insert(key, str(key))
    printree(tree.root)