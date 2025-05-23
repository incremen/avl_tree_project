import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from avl_tree import AVLTree
from bst import BSTree
import matplotlib.pyplot as plt

    
def generate_sorted(n):
    return list(range(n))


def generate_reversed(n):
    return list(range(n - 1, -1, -1))


def time_insertion(tree_class, start_mode, data):
    t0 = time.time()
    tree = tree_class()
    for val in data:
        tree.insert(val, str(val), start=start_mode)
    t1 = time.time()
    return t1 - t0

def run_all_experiments(sizes, repeats=5):
    results = []

    for n in sizes:
        sorted_data = generate_sorted(n)
        reversed_data = generate_reversed(n)

        scenarios = [
            ("BST", "root", sorted_data),
            ("BST", "root", reversed_data),
            ("BST", "max", sorted_data),
            ("BST", "max", reversed_data),
            ("AVL", "root", sorted_data),
            ("AVL", "root", reversed_data),
            ("AVL", "max", sorted_data),
            ("AVL", "max", reversed_data),
        ]

        print(f"\n--- Size n = {n} ---")
        for tree_type, start_mode, data in scenarios:
            total_time = 0
            for _ in range(repeats):
                if tree_type == "BST":
                    total_time += time_insertion(BSTree, start_mode, data)
                else:
                    total_time += time_insertion(AVLTree, start_mode, data)
            avg_time = total_time / repeats
            results.append((tree_type, start_mode, "sorted" if data == sorted_data else "reversed", n, avg_time))
            print(f"{tree_type} Tree, Start = {start_mode}, Input = {'sorted' if data == sorted_data else 'reversed'} → {avg_time:.6f} seconds")

    return results

def plot_results(results, folder):
    # Separate results by input type
    sorted_results = [r for r in results if r[2] == 'sorted']
    reversed_results = [r for r in results if r[2] == 'reversed']
    
    def plot_scenario(data, input_type):
        plt.figure(figsize=(10, 6))
        for tree_type in ['BST', 'AVL']:
            for start_mode in ['root', 'max']:
                y = [r[4] for r in data if r[0] == tree_type and r[1] == start_mode]
                x = [r[3] for r in data if r[0] == tree_type and r[1] == start_mode]
                label = f"{tree_type} ({start_mode})"
                plt.plot(x, y, marker='o', label=label)
        plt.xlabel('n (number of elements)')
        plt.ylabel('Average Insertion Time (seconds)')
        plt.title(f'Insertion Time vs n ({input_type.capitalize()} Data)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        out_path = os.path.join(folder, f'insertion_time_{input_type}.png')
        plt.savefig(out_path)
        plt.close()
        print(f"Saved graph: {out_path}")

    plot_scenario(sorted_results, 'sorted')
    plot_scenario(reversed_results, 'reversed')

sizes_to_test = [10,50, 100, 500, 1000, 5000]
results = run_all_experiments(sizes_to_test)
plot_results(results, os.path.dirname(__file__))