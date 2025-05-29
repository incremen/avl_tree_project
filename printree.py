## This file contains functions for the representation of binary trees.
## Used in class Binary_search_tree's __repr__
## Written by a former student in the course - thanks to Amitai Cohen
## No need to fully understand this code

def printree(t, file=None, append=True, bykey=True):
    """Print a textual representation of t
    bykey=True: show keys instead of values, and also show balance factor
    file: if provided (as a filename), write output to this file (file is always cleared first)"""
    rows = trepr(t, bykey)
    mode = "a" if append else "w"
    if file:
        with open(file, mode) as f:
            for row in rows:
                print(row)
                print(row, file=f)
    else:
        for row in rows:
            print(row)

def trepr(t, bykey=False):
    """Return a list of textual representations of the levels in t
    bykey=True: show keys instead of values, and also show balance factor and zero_balance_count"""
    if t is None:
        return ["#"]

    # Show key, balance factor, zero_balance_count, and height in compact form
    if hasattr(t, 'key') and hasattr(t, 'balance_factor') and hasattr(t, 'zero_balance_count') and hasattr(t, 'height'):
        val = str(t.key) if bykey else str(getattr(t, 'value', getattr(t, 'val', t)))
        bf = t.balance_factor() if callable(t.balance_factor) else t.balance_factor
        zbf = t.zero_balance_count
        h = t.height
        thistr = f"{val},({bf}),[{zbf}]{{{h}}}"
    else:
        thistr = str(getattr(t, 'key', t)) if bykey else str(getattr(t, 'val', t))

    return conc(trepr(getattr(t, 'left', None), bykey), thistr, trepr(getattr(t, 'right', None), bykey))

def conc(left, root, right):
    """Return a concatenation of textual representations of
    a root node, its left node, and its right node
    root is a string, and left and right are lists of strings"""

    lwid = len(left[-1])
    rwid = len(right[-1])
    rootwid = len(root)

    result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

    ls = leftspace(left[0])
    rs = rightspace(right[0])
    result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "|" + rs * "_" + (rwid - rs) * " ")

    for i in range(max(len(left), len(right))):
        row = ""
        if i < len(left):
            row += left[i]
        else:
            row += lwid * " "

        row += (rootwid + 2) * " "

        if i < len(right):
            row += right[i]
        else:
            row += rwid * " "

        result.append(row)

    return result

def leftspace(row):
    """helper for conc"""
    # row is the first row of a left node
    # returns the index of where the second whitespace starts
    i = len(row) - 1
    while i >= 0 and row[i] == " ":
        i -= 1
    return i + 1

def rightspace(row):
    """helper for conc"""
    # row is the first row of a right node
    # returns the index of where the first whitespace ends
    i = 0
    while i < len(row) and row[i] == " ":
        i += 1
    return i