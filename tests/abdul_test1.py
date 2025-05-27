import traceback
import unittest
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 🔧 Update this import to match the actual location / name of your AVL implementation
# from avl_tree import AVLTree  # noqa: F401 – replace 'avl' with your module name if different
from new_avl_tree_with_fixed_delete import AVLTree  # noqa: F401 – replace 'old_avl_tree_code' with your module name if different

def tree_to_str(tree):
    root = tree.get_root()
    return '\n'.join(printree(root))


def printree(root):
    if root is None or not root.is_real_node():
        return ["#"]

    root_key = str(f'k {root.key}, h {root.height}')
    left, right = printree(root.left), printree(root.right)

    lwid = len(left[-1])
    rwid = len(right[-1])
    rootwid = len(root_key)

    result = [(lwid + 1) * " " + root_key + (rwid + 1) * " "]

    ls = len(left[0].rstrip())
    rs = len(right[0]) - len(right[0].lstrip())
    result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

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


# -----------------------------------------------------------------------------
# Helper wrappers – adapt only if your node/AVL API differs
# -----------------------------------------------------------------------------

def _is_real(node):
    if node is None:
        return False
    if hasattr(node, "is_real_node"):
        return node.is_real_node()
    if hasattr(node, "isRealNode"):
        return node.isRealNode()
    return getattr(node, "key", None) is not None

def _get_left(node):
    return node.get_left() if hasattr(node, "get_left") else getattr(node, "left", None)

def _get_right(node):
    return node.get_right() if hasattr(node, "get_right") else getattr(node, "right", None)

def _get_height(node):
    if node is None or not _is_real(node):
        return -1
    if hasattr(node, "get_height"):
        return node.get_height()
    return getattr(node, "height", -1)

def _get_value(node):
    if hasattr(node, "get_value"):
        return node.get_value()
    return getattr(node, "value", None)

# -----------------------------------------------------------------------------
#                              Test Suite
# -----------------------------------------------------------------------------

class TestAVLTree(unittest.TestCase):
    """Functional & structural tests for AVLTree, including Amir‑BF, get_root, size."""

    # ------------------------------------------------------------------
    # Boilerplate setup + logging helpers
    # ------------------------------------------------------------------
    def setUp(self):
        self.tree = AVLTree()
        self.last_op = None      # textual description of the last op
        self.before_state = None # tree string before the op

    def _record_state(self):
        """Save state of the tree (string) before mutating op."""
        try:
            self.before_state = tree_to_str(self.tree)
        except Exception:
            self.before_state = "(tree_to_str failed)"

    def _report_error(self, exc):
        """Append detailed error info to avl_error_log.txt and re‑raise."""
        with open("avl_error_log.txt", "a", encoding="utf‑8") as f:
            f.write("\n==============================\n")
            f.write("Exception during test:\n")
            f.write(traceback.format_exc())
            f.write(f"Last operation: {self.last_op}\n\n")
            f.write("State before operation:\n")
            f.write(self.before_state or "(unavailable)")
            f.write("\nState after operation:\n")
            try:
                f.write(tree_to_str(self.tree))
            except Exception as rep_err:
                f.write(f"[tree_to_str failed: {rep_err}]")
            f.write("\n==============================\n")

    # ------------------------------------------------------------------
    # Structural invariant check
    # ------------------------------------------------------------------
    def _assert_avl_invariants(self, node):
        if node is None or not _is_real(node):
            return -1
        lh = self._assert_avl_invariants(_get_left(node))
        rh = self._assert_avl_invariants(_get_right(node))
        self.assertLessEqual(abs(lh - rh), 1,
                             f"Unbalanced at key {_get_value(node)}: {lh=} {rh=}")
        stored_h = _get_height(node)
        if stored_h != -1:
            self.assertEqual(stored_h, max(lh, rh) + 1,
                             f"Height mismatch at key {_get_value(node)}")
        return max(lh, rh) + 1

    # ------------------------------------------------------------------
    # Convenience: insert a batch of keys
    # ------------------------------------------------------------------
    def _insert_keys(self, keys):
        for k in keys:
            self.last_op = f"insert({k},{k})"
            self._record_state()
            reb = self.tree.insert(k, str(k), "max")
            self.assertIsInstance(reb, int)
            self.assertGreaterEqual(reb, 0)

    # ------------------------------------------------------------------
    # Core dictionary behaviour
    # ------------------------------------------------------------------
    def test_single_insert_and_search(self):
        try:
            self.last_op = "insert(10,'a')"
            self._record_state()
            self.tree.insert(10, "a")
            self.assertEqual(_get_value(self.tree.search(10)), "a")
            self.assertEqual(self.tree.avl_to_array(), [(10, "a")])
        except Exception as e:
            self._report_error(e)
            raise

    def test_search_missing_key(self):
        try:
            self._insert_keys([1])
            self.last_op = "search(99)"
            self._record_state()
            self.assertIsNone(self.tree.search(99))
        except Exception as e:
            self._report_error(e)
            raise

    def test_multiple_inserts_sorted_order_and_structure(self):
        try:
            keys = [5, 2, 8, 1, 3, 7, 9]
            self._insert_keys(keys)
            self.assertEqual(self.tree.avl_to_array(), sorted((k, str(k)) for k in keys))
            root = self.tree.get_root()
            if root is not None:
                self._assert_avl_invariants(root)
        except Exception as e:
            self._report_error(e)
            raise

    # ------------------------------------------------------------------
    # Delete scenarios
    # ------------------------------------------------------------------
    def test_delete_leaf_and_structure(self):
        try:
            self._insert_keys([10, 5, 15])
            leaf = self.tree.search(5)
            self.last_op = "delete(5)"
            self._record_state()
            self.tree.delete(leaf)
            self.assertEqual(self.tree.avl_to_array(), [(10, "10"), (15, "15")])
            self._assert_avl_invariants(self.tree.get_root())
        except Exception as e:
            self._report_error(e)
            raise

    def test_random_insert_delete_structure(self):
        try:
            keys = list(range(60))
            random.shuffle(keys)
            self._insert_keys(keys)
            # delete half randomly
            random.shuffle(keys)
            for k in keys[:30]:
                node = self.tree.search(k)
                self.last_op = f"delete({k})"
                self._record_state()
                self.tree.delete(node)
            self._assert_avl_invariants(self.tree.get_root())
        except Exception as e:
            self._report_error(e)
            raise

    # ------------------------------------------------------------------
    # get_root & size
    # ------------------------------------------------------------------
    def test_get_root_and_size(self):
        try:
            # empty tree
            self.assertIsNone(self.tree.get_root())
            self.assertEqual(self.tree.size(), 0)
            # after inserts
            self._insert_keys([4, 2, 6])
            self.assertIsNotNone(self.tree.get_root())
            self.assertEqual(self.tree.size(), 3)
            # after deleting all
            for k in [4, 2, 6]:
                self.last_op = f"delete({k})"
                self._record_state()
                self.tree.delete(self.tree.search(k))
            self.assertIsNone(self.tree.get_root())
            self.assertEqual(self.tree.size(), 0)
        except Exception as e:
            self._report_error(e)
            raise

    # ------------------------------------------------------------------
    # Amir balance‑factor ratio
    # ------------------------------------------------------------------
    def _manual_amir_ratio(self):
        """Helper: compute ratio manually from current tree."""
        def dfs(node):
            if not _is_real(node):
                return 0, 0
            l_tot, l_zero = dfs(_get_left(node))
            r_tot, r_zero = dfs(_get_right(node))
            total = 1 + l_tot + r_tot
            zeros = l_zero + r_zero + (1 if getattr(node, "get_bf")() == 0 else 0)
            return total, zeros
        total, zeros = dfs(self.tree.get_root())
        return zeros / total if total else 0.0

    def test_amir_balance_factor_accuracy(self):
        try:
            # empty
            self.assertEqual(self.tree.get_amir_balance_factor(), 0.0)
            # random tree – compare to manual
            keys = list(range(25))
            random.shuffle(keys)
            self._insert_keys(keys)
            self.assertAlmostEqual(self.tree.get_amir_balance_factor(), self._manual_amir_ratio(), places=6)
            # after deletions
            for k in keys[:10]:
                self.last_op = f"delete({k})"
                self._record_state()
                self.tree.delete(self.tree.search(k))
            self.assertAlmostEqual(self.tree.get_amir_balance_factor(), self._manual_amir_ratio(), places=6)
        except Exception as e:
            self._report_error(e)
            raise


if __name__ == "__main__":
    unittest.main(verbosity=2)