from avl_tree import AVLTree
from printree import printree
import random

def print_and_log(msg, file="tree_output.txt"): 
    print(msg)
    with open(file, "a") as f:
        f.write(str(msg) + "\n")

def test_random_tree():
    tree = AVLTree()
    keys = list(range(60))
    random.shuffle(keys)
    for key in keys:
        tree.insert(key, str(key), "max")


    printree(tree.root, file = "tree_output.txt", )


def test_sequential_inserts():
    tree = AVLTree()
    with open("tree_output.txt", "w") as f:
        f.write("--- Inserting 0 to 11 ---\n")
    for i in range(12):
        tree.insert(i, str(i))
        print_and_log(f"\n=== After Inserting {i} ===\nTree size: {tree.size()}")
        printree(tree.root, file="tree_output.txt", append=True)

    print_and_log("\n--- Deleting even numbers 0 to 10 ---")
    for i in range(0, 12, 2):
        node = tree.search(i)
        if node:
            print_and_log(f"\n=== Before Deleting {i} ===\nTree size: {tree.size()}\nNode found: key={node.key}, value={node.value}, parent={getattr(node.parent, 'key', None)}, left={getattr(node.left, 'key', None)}, right={getattr(node.right, 'key', None)}")
        else:
            print_and_log(f"\n=== Before Deleting {i} ===\nTree size: {tree.size()}\nNode not found!")
        printree(tree.root, file="tree_output.txt", append=True)
        try:
            tree.delete(node)
            print_and_log(f"Deleted {i} successfully.")
        except Exception as e:
            print_and_log(f"Exception during delete: {e}")
        print_and_log(f"\n=== After Deleting {i} ===\nTree size: {tree.size()}")
        printree(tree.root, file="tree_output.txt", append=True)


if __name__ == "__main__":
    test_sequential_inserts()
