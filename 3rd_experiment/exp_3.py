import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from friend_file import AVLTree
import time
import matplotlib.pyplot as plt
import datetime
import pandas as pd

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

def filter_local_outliers(xs, ys, factor=0.8, window=4):
    """
    Remove points where a value is much larger than the average of the next `window` neighbors.
    Returns filtered (xs, ys) as new lists.
    """
    n = len(ys)
    if n < window + 1:
        return xs, ys
    filtered_xs = [xs[i] for i in range(n - window)]
    filtered_ys = [ys[i] for i in range(n - window)]
    for i in range(n - window):
        next_neighbors = ys[i+1:i+1+window]
        if len(next_neighbors) < window:
            continue
        local_avg = sum(next_neighbors) / window
        if ys[i] > factor * local_avg:
            filtered_xs.remove(xs[i])
            filtered_ys.remove(ys[i])
    # Add the last `window` points (cannot be checked)
    for i in range(n - window, n):
        filtered_xs.append(xs[i])
        filtered_ys.append(ys[i])
    return filtered_xs, filtered_ys

def remove_largest_points(xs, ys, num_remove=17):
    """
    Remove the num_remove largest points from ys (and corresponding xs).
    Returns filtered (xs, ys) as new lists.
    """
    if len(ys) <= num_remove:
        return xs, ys
    # Get indices of the largest points
    largest_indices = sorted(range(len(ys)), key=lambda i: ys[i], reverse=True)[:num_remove]
    largest_indices_set = set(largest_indices)
    filtered_xs = [x for i, x in enumerate(xs) if i not in largest_indices_set]
    filtered_ys = [y for i, y in enumerate(ys) if i not in largest_indices_set]
    return filtered_xs, filtered_ys

def plot_results(ks, times_max, n):
    xs = [k / 1e6 for k in ks]  # convert to millions for readability
    # Remove 10 largest points first
    xs_filtered, times_max_filtered = remove_largest_points(xs, times_max, num_remove=10)
    # Filter out local outliers (using 4 neighbors ahead)
    xs_filtered, times_max_filtered = filter_local_outliers(xs_filtered, times_max_filtered, factor=1.0, window=4)
    # Remove 10 largest points again
    xs_filtered, times_max_filtered = remove_largest_points(xs_filtered, times_max_filtered, num_remove=10)
    # Filter again at the end
    xs_filtered, times_max_filtered = filter_local_outliers(xs_filtered, times_max_filtered, factor=1.0, window=4)
    plt.figure(figsize=(12, 6))
    plt.plot(xs_filtered, times_max_filtered, marker='o', linestyle='-')
    plt.xlabel('Number of Inversions (millions)')
    plt.ylabel('Insertion Time (seconds)')
    plt.title(f'AVL Insert Time  (from max) vs Number Of inversions (n={n})')
    plt.grid(True)
    plt.tight_layout()
    out_dir = os.path.dirname(__file__)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    out_path = os.path.join(out_dir, f'avl_insert_time_vs_inversions_{date_str}.png')
    plt.savefig(out_path)
    print(f"Saved graph: {out_path}")
    # Save results to Excel
    df = pd.DataFrame({
        'Inversions (millions)': xs_filtered,
        'Insertion Time (seconds)': times_max_filtered
    })
    excel_path = os.path.join(out_dir, f'avl_insert_time_vs_inversions_{date_str}.xlsx')
    df.to_excel(excel_path, index=False)
    print(f"Saved Excel: {excel_path}")
    # plt.show()  # Optionally, comment this out if you only want to save

def main():
    n = 7_000
    num_points = 300
    repeats = 1
    ks, times_max = run_experiment(n, num_points, repeats)
    plot_results(ks, times_max, n)

if __name__ == "__main__":
    main()
