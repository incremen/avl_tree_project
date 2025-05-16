from avl_tree import AVLTree
from printree import printree

def check_heights(node):
    if node is None or not node.is_real_node():
        return -1
    lh = check_heights(node.left)
    rh = check_heights(node.right)
    expected = max(lh, rh) + 1
    if node.height != expected:
        print(f"Height mismatch at key {node.key}: stored {node.height}, expected {expected}")
    return expected

if __name__ == "__main__":
    tree = AVLTree()
    keys = [i for i in range(57)]
    for key in keys:
        tree.insert(key, str(key))
    printree(tree.root, "tree_output.txt")
    print("\nChecking heights:")
    check_heights(tree.root)