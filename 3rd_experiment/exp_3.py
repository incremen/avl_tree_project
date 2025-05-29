import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from avl_tree import AVLTree
import time
import matplotlib.pyplot as plt
import datetime

def generate_permutation(n, k):
    """Generate a permutation of size n with exactly k inversions."""
    inv = []
    remaining = k
    for i in range(n):
        max_inv = n - 1 - i
        val = min(remaining, max_inv)
        inv.append(val)
        remaining -= val
    perm = []
    for i in range(n, 0, -1):
        perm.insert(inv[n - i], i)
    return perm

def run_experiment(n, num_points=80, repeats=1):
    max_inv = n * (n - 1) // 2
    ks = [int(i * max_inv / (num_points - 1)) for i in range(num_points)]
    times_max = []
    for k in ks:
        total_time = 0
        for _ in range(repeats):
            perm = generate_permutation(n, k)
            tree = AVLTree()
            start_time = time.perf_counter()
            for x in perm:
                tree.insert(x, str(x), start="max")
            end_time = time.perf_counter()
            total_time += (end_time - start_time)
        avg_time = total_time / repeats
        times_max.append(avg_time)
    return ks, times_max

def plot_results(ks, times_max, n):
    xs = [k / 1e6 for k in ks]  # convert to millions for readability
    # Filter out bad points before plotting
    xs_filtered, times_max_filtered = filter_out_bad_points(xs, times_max)
    plt.figure(figsize=(12, 6))
    plt.plot(xs_filtered, times_max_filtered, marker='o', linestyle='-')
    plt.xlabel('Number of Inversions (millions)')
    plt.ylabel('Insertion Time (seconds)')
    plt.title(f'AVL Insert Time vs Number of Inversions (n={n}, 50 samples, start="max")')
    plt.grid(True)
    plt.tight_layout()
    out_dir = os.path.dirname(__file__)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    out_path = os.path.join(out_dir, f'avl_insert_time_vs_inversions_{date_str}.png')
    plt.savefig(out_path)
    print(f"Saved graph: {out_path}")
    # plt.show()  # Optionally, comment this out if you only want to save

def filter_out_bad_points(xs, ys):
    """
    Remove points where a value is greater than the sum of its neighbors.
    Returns filtered (xs, ys) as new lists.
    """
    if len(ys) < 3:
        return xs, ys
    filtered_xs = [xs[0]]
    filtered_ys = [ys[0]]
    for i in range(1, len(ys) - 1):
        if ys[i] <= ys[i - 1] + ys[i + 1]:
            filtered_xs.append(xs[i])
            filtered_ys.append(ys[i])
    filtered_xs.append(xs[-1])
    filtered_ys.append(ys[-1])
    return filtered_xs, filtered_ys 

def main():
    n = 7_000
    num_points = 90
    repeats = 1
    ks, times_max = run_experiment(n, num_points, repeats)
    plot_results(ks, times_max, n)

if __name__ == "__main__":
    main()
