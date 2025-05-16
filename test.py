from adam_avl_tree import AVLTree
from printree import printree

if __name__ == "__main__":
    tree = AVLTree()
    for key in [30, 20, 40, 10, 25, 35, 50]:
        tree.insert(key, str(key))
    printree(tree.root)