import time
import sys
import os
import concurrent.futures
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bst import BSTree
# from avl_tree import AVLTree
from friend_file import AVLTree



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

def run_scenario(args):
    tree_type, start_mode, data, n, repeats = args
    total_time = 0
    for _ in range(repeats):
        if tree_type == "BST":
            total_time += time_insertion(BSTree, start_mode, data)
        else:
            total_time += time_insertion(AVLTree, start_mode, data)
    avg_time = total_time / repeats
    return (tree_type, start_mode, "sorted" if data == list(range(n)) else "reversed", n, avg_time)


def run_all_experiments(sizes, repeats=1):
    scenarios = [("BST", "root"), ("BST", "max"), ("AVL", "root"), ("AVL", "max")]
    tasks = []
    for n in sizes:
        sorted_data = generate_sorted(n)
        reversed_data = generate_reversed(n)
        for tree_type, start_mode in scenarios:
            tasks.append((tree_type, start_mode, sorted_data, n, repeats))
            tasks.append((tree_type, start_mode, reversed_data, n, repeats))
    results = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for res in executor.map(run_scenario, tasks):
            results.append(res)
    return results

def run_sorted_experiments(sizes, repeats=5):
    scenarios = [("BST", "root"), ("BST", "max"), ("AVL", "root"), ("AVL", "max")]
    tasks = []
    for n in sizes:
        sorted_data = generate_sorted(n)
        for tree_type, start_mode in scenarios:
            tasks.append((tree_type, start_mode, sorted_data, n, repeats))
    results = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for res in executor.map(run_scenario, tasks):
            results.append(res)
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
                # Add labels to each point in base 10
                for i, j in zip(x, y):
                    plt.text(i, j, f"{j:.6f}", fontsize=8, ha='right')
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

if __name__ == "__main__":
    import time
    sizes_to_test = [50* i for i in range(1, 40)]
    start_time = time.time()
    results = run_all_experiments(sizes_to_test)
    # results = run_sorted_experiments(sizes_to_test)
    plot_results(results, os.path.dirname(__file__))
    end_time = time.time()
    print(f"\nTotal experiment time: {end_time - start_time:.2f} seconds")