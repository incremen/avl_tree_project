from avl_tree import AVLTree
from printree import printree
import random

def test_random_tree():
    tree = AVLTree()
    keys = list(range(60))
    random.shuffle(keys)
    for key in keys:
        tree.insert(key, str(key), "max")


    printree(tree.root, file = "tree_output.txt", )


if __name__ == "__main__":
    test_random_tree()
