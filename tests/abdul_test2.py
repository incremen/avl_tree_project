import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from avl_tree import AVLNode, AVLTree


class TestAdvancedAVLTree(unittest.TestCase):

    def setUp(self):
        self.tree = AVLTree()

    def test_sorted_inserts_balanced(self):
        # Insert sorted keys to test worst-case scenario (linked list in BST)
        keys = list(range(10))
        rotations = 0
        for key in keys:
            rotations += self.tree.insert(key, str(key))
        self.assertTrue(rotations > 0, "Expected rotations due to imbalance")
        self.assertEqual(self.tree.size(), 10)
        self.assertTrue(self.tree.get_root().key == 3 or self.tree.get_root().key == 4)

    def test_balancing_multiple_patterns(self):
        # Test left-right and right-left cases
        self.tree.insert(10, "10")
        self.tree.insert(5, "5")
        self.tree.insert(7, "7")  # Causes left-right
        self.assertEqual(self.tree.get_root().key, 7)

        self.tree = AVLTree()  # Reset
        self.tree.insert(5, "5")
        self.tree.insert(10, "10")
        self.tree.insert(8, "8")  # Causes right-left
        self.assertEqual(self.tree.get_root().key, 8)

    def test_height_and_balance(self):
        keys = [20, 10, 30, 5, 15, 25, 35]
        for key in keys:
            self.tree.insert(key, str(key))
        self.assertEqual(self.tree.get_root().height, 2)
        # Every node must be balanced
        def check_balances(node):
            if node and node.is_real_node():
                balance = self.tree._get_balance(node)
                self.assertIn(balance, [-1, 0, 1], f"Node {node.key} has balance {balance}")
                check_balances(node.left)
                check_balances(node.right)
        check_balances(self.tree.get_root())

    def test_delete_leaf(self):
        self.tree.insert(20, "20")
        self.tree.insert(10, "10")
        self.tree.insert(30, "30")
        leaf = self.tree.search(10)
        self.assertTrue(leaf is not None)
        rotations = self.tree.delete(leaf)
        self.assertEqual(self.tree.size(), 2)
        self.assertTrue(rotations >= 0)

    def test_delete_internal_node(self):
        keys = [20, 10, 30, 25, 35]
        for key in keys:
            self.tree.insert(key, str(key))
        to_delete = self.tree.search(30)
        self.assertTrue(to_delete is not None)
        self.tree.delete(to_delete)
        self.assertIsNone(self.tree.search(30))
        self.assertEqual(self.tree.size(), 4)

    def test_zero_balance_factor_ratio(self):
        keys = [50, 25, 75, 10, 30, 60, 80]
        for key in keys:
            self.tree.insert(key, str(key))
        ratio = self.tree.get_amir_balance_factor()
        self.assertTrue(0 <= ratio <= 1)
        self.assertIsInstance(ratio, float)

    def test_search_not_found(self):
        self.tree.insert(5, "5")
        self.tree.insert(10, "10")
        self.assertIsNone(self.tree.search(999))

    def test_inorder_array_sorted(self):
        keys = [7, 2, 9, 1, 5, 8, 10]
        for key in keys:
            self.tree.insert(key, str(key))
        arr = self.tree.avl_to_array()
        sorted_keys = [x[0] for x in arr]
        self.assertEqual(sorted_keys, sorted(keys))


if __name__ == "__main__":
    unittest.main()
