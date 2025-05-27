from avl_tree import AVLTree
from printree import printree
import random

def check_heights(node):
    if node is None or not node.is_real_node():
        return -1
    lh = check_heights(node.left)
    rh = check_heights(node.right)
    expected = max(lh, rh) + 1
    if node.height != expected:
        print(f"Height mismatch at key {node.key}: stored {node.height}, expected {expected}")
    return expected

def test_random_insert_delete():
    tree = AVLTree()
    keys = list(range(60))
    random.shuffle(keys)
    for key in keys:
        tree.insert(key, str(key), "max")
    # delete half randomly
    random.shuffle(keys)
    # for k in keys[:30]:
    #     node = tree.search(k)
    #     tree.delete(node)

    printree(tree.root, file = "tree_output.txt")


if __name__ == "__main__":
    print("Testing random insert and delete...")
    test_random_insert_delete()
    print("Random insert and delete test completed.")
