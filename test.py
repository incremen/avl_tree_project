from avl_tree import AVLTree
from printree import printree

if __name__ == "__main__":
    tree = AVLTree()
    for key in [1, 2, 3, 4, 5, 6, 7, 8, 9,10]:
        tree.insert(key, str(key))
        printree(tree.root, "tree_output.txt")