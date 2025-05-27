import time
import sys
import os
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bst import BSTree
from new_avl_tree_with_fixed_delete import AVLTree

def generate_sorted(n):
    return list(range(n))

def time_insertion(tree_class, start_mode, data):
    t0 = time.time()
    tree = tree_class()
    for val in data:
        tree.insert(val, str(val), start=start_mode)
    t1 = time.time()
    return t1 - t0

def run_experiment(sizes, repeats=5):
    results = {"AVL_sorted": [], "AVL_max": [], "BST_max": []}
    for n in sizes:
        sorted_data = generate_sorted(n)
        # AVL insert from root (sorted order)
        avl_sorted_time = sum(time_insertion(AVLTree, "root", sorted_data) for _ in range(repeats)) / repeats
        # AVL insert from max (sorted order)
        avl_max_time = sum(time_insertion(AVLTree, "max", sorted_data) for _ in range(repeats)) / repeats
        # BST insert from max (sorted order)
        bst_max_time = sum(time_insertion(BSTree, "max", sorted_data) for _ in range(repeats)) / repeats
        results["AVL_sorted"].append((n, avl_sorted_time))
        results["AVL_max"].append((n, avl_max_time))
        results["BST_max"].append((n, bst_max_time))
    return results

def plot_results(results, folder):
    plt.figure(figsize=(10, 6))
    for label, data in results.items():
        x = [item[0] for item in data]
        y = [item[1] for item in data]
        plt.plot(x, y, marker='o', label=label.replace('_', ' '))
        for i, j in zip(x, y):
            plt.text(i, j, f"{j:.6f}", fontsize=8, ha='right')
    plt.xlabel('n (number of elements)')
    plt.ylabel('Average Insertion Time (seconds)')
    plt.title('Insertion Time Comparison (Sorted Input)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    out_path = os.path.join(folder, 'insertion_time_comparison_sorted.png')
    plt.savefig(out_path)
    plt.close()
    print(f"Saved graph: {out_path}")

if __name__ == "__main__":
    sizes_to_test = [10, 50, 100, 200, 500, 1000, 1500, 1700, 2000, 2500, 3000, 3500, 4000]
    start_time = time.time()
    results = run_experiment(sizes_to_test)
    plot_results(results, os.path.dirname(__file__))
    end_time = time.time()
    print(f"\nTotal experiment time: {end_time - start_time:.2f} seconds")
