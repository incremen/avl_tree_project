import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from avl_tree import AVLTree, AVLNode
from friend_file import AVLTree  # noqa: F401 – replace 'old_avl_tree_code' with your module name if different

class TestAdvancedAVLTree(unittest.TestCase):

    def setUp(self):
        self.tree = AVLTree()

    def test_heavy_insert_delete_mixed(self):
        # Insert 1000 keys
        for i in range(1000):
            self.tree.insert(i, str(i))
        self.assertEqual(self.tree.size(), 1000)

        # Delete even keys
        for i in range(0, 1000, 2):
            node = self.tree.search(i)
            self.assertIsNotNone(node)
            self.tree.delete(node)

        self.assertEqual(self.tree.size(), 500)
        for i in range(0, 1000, 2):
            self.assertIsNone(self.tree.search(i))
        for i in range(1, 1000, 2):
            self.assertEqual(self.tree.search(i).value, str(i))

    def test_rebalancing_rotations(self):
        # This specific order should cause multiple rotations
        insert_order = [10, 20, 30, 40, 50, 25]
        for key in insert_order:
            self.tree.insert(key, str(key))
        self.assertEqual(self.tree.size(), 6)

        # Confirm tree remains balanced (BF between -1 and 1)
        def check_balance(node):
            if node is None or not node.is_real_node():
                return True
            bf = self.tree._get_balance(node)
            self.assertIn(bf, [-1, 0, 1])
            check_balance(node.left)
            check_balance(node.right)

        check_balance(self.tree.get_root())

    def test_delete_root_until_empty(self):
        keys = [50, 30, 70, 20, 40, 60, 80]
        for k in keys:
            self.tree.insert(k, str(k))

        while self.tree.size() > 0:
            root = self.tree.get_root()
            self.tree.delete(root)

        self.assertIsNone(self.tree.get_root())
        self.assertEqual(self.tree.size(), 0)

    def test_max_node_tracking(self):
        keys = [15, 10, 20, 25, 8, 12]
        for k in keys:
            self.tree.insert(k, str(k))

        max_node = self.tree.get_max_node()
        self.assertEqual(max_node.key, 25)

        self.tree.delete(self.tree.search(25))
        self.assertEqual(self.tree.get_max_node().key, 20)

    def test_avl_to_array_sorted(self):
        import random
        values = list(range(50))
        random.shuffle(values)
        for val in values:
            self.tree.insert(val, str(val))

        arr = self.tree.avl_to_array()
        sorted_keys = [k for k, v in arr]
        self.assertEqual(sorted_keys, list(range(50)))

    def test_amir_balance_factor_values(self):
        for i in range(1, 21):
            self.tree.insert(i, str(i))

        bf = self.tree.get_amir_balance_factor()
        self.assertGreaterEqual(bf, 0)
        self.assertLessEqual(bf, 1)

        # Balance factor must be in range [0,1]
        self.assertTrue(0 <= bf <= 1)

if __name__ == '__main__':
    unittest.main()
