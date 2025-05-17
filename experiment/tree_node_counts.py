import pandas as pd

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

n_values = list(range(1, 31))  # You can increase the upper limit for bigger n
leaves = [fib(n + 1) for n in n_values]
nodes = [fib(n + 3) - 1 for n in n_values]
ratio = [l / n for n, l in zip(nodes, leaves)]  # Inverse ratio: leaves/nodes

# Create a table for n, nodes, leaves, and inverse ratio
ratio_table = pd.DataFrame({
    'n': n_values,
    'count (nodes)': nodes,
    'leaves': leaves,
    'ratio (leaves/nodes)': ratio
})
print(ratio_table.to_string(index=False))

# Save as Excel file
ratio_table.to_excel('experiment/fib_tree_table.xlsx', index=False)
# Save as PNG image (table)
try:
    import dataframe_image as dfi
    dfi.export(ratio_table, 'experiment/fib_tree_table.png')
except ImportError:
    print('Install dataframe_image to export as PNG: pip install dataframe_image')
