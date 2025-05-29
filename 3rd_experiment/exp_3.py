import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Re-import AVLTree after state reset
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

# Parameters
n = 10000
max_inv = n * (n - 1) // 2
num_points = 100
# Generate 100 evenly spaced inversion counts
ks = [int(i * max_inv / (num_points - 1)) for i in range(num_points)]

times_max = []
for k in ks:
    perm = generate_permutation(n, k)
    tree = AVLTree()
    start_time = time.perf_counter()
    for x in perm:
        tree.insert(x, str(x), start="max")
    end_time = time.perf_counter()
    times_max.append(end_time - start_time)

# Plotting
xs = [k / 1e6 for k in ks]  # convert to millions for readability
plt.figure(figsize=(12, 6))
plt.plot(xs, times_max, marker='o', linestyle='-')
plt.xlabel('Number of Inversions (millions)')
plt.ylabel('Insertion Time (seconds)')
plt.title(f'AVL Insert Time vs Number of Inversions (n={n}, 50 samples, start="max")')
plt.grid(True)
plt.tight_layout()

# Save figure with date in filename
out_dir = os.path.dirname(__file__)
date_str = datetime.datetime.now().strftime("%Y-%m-%d")
out_path = os.path.join(out_dir, f'avl_insert_time_vs_inversions_{date_str}.png')
plt.savefig(out_path)
print(f"Saved graph: {out_path}")
# plt.show()  # Optionally, comment this out if you only want to save
