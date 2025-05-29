# =============================
# AVL Tree Implementation
# =============================

from typing import Optional, List, Tuple

#username - complete info
#id1      - complete info 
#name1    - complete info 
#id2      - complete info
#name2    - complete info  

"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int or None
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """
    def __init__(self, key: Optional[int], value: Optional[str], is_a_virtual_node: bool = False):
        self.key: Optional[int] = key
        self.value: Optional[str] = value
        self.parent: Optional['AVLNode'] = None
        self.left: Optional['AVLNode'] = None if is_a_virtual_node else VirtualAVLNode.get_create_instance()
        self.right: Optional['AVLNode'] = None if is_a_virtual_node else VirtualAVLNode.get_create_instance()
        self.height: int = 0 if not is_a_virtual_node else -1
        self.is_balanced: bool = True if not is_a_virtual_node else False

    def is_real_node(self) -> bool:
        return True
    
    def get_bf(self) -> int:
        return self.left.height - self.right.height


# =============================
# Virtual Node Singleton
# =============================

class VirtualAVLNode(AVLNode):
    singleton_object: Optional['VirtualAVLNode'] = None

    def __init__(self):
        super().__init__(None, None, True)
        # singleton_object = None  # Not needed

    @staticmethod
    def get_create_instance() -> 'VirtualAVLNode':
        if VirtualAVLNode.singleton_object is None:
            VirtualAVLNode.singleton_object = VirtualAVLNode()
        return VirtualAVLNode.singleton_object

    def is_real_node(self) -> bool:
        return False


# =============================
# Utility Functions
# =============================

def get_balance(node: AVLNode) -> int:
    return node.left.height - node.right.height


def min_node_of(node: AVLNode) -> AVLNode:
    while node.left.is_real_node():
        node = node.left
    return node


# =============================
# AVL Tree Class
# =============================

class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """
    def __init__(self):
        self.root: AVLNode = VirtualAVLNode.get_create_instance()
        self.max: AVLNode = self.root
        self._size: int = 0
        self._balanced_nodes: int = 0

    # --- Search Methods ---
    def search(self, key: int) -> Optional[AVLNode]:
        node = self.root
        while node.is_real_node():
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None
    
    def find(self, key: int) -> Optional[AVLNode]:
        """Alias for search method."""
        return self.search(key)

    # --- Insertion Methods ---
    def insert(self, key: int, val: str, start: str = "root") -> int:
        # Handle empty tree case
        if not self.root.is_real_node():
            self.create_root(key, val)
            return 0

        # Choose starting point
        current = self.root if start == "root" else self.max

        # If starting from max, climb UP until we're at a node whose subtree should contain the new key
        if start == "max":
            while current != self.root and current.key > key and current.parent:
                current = current.parent

        # Now do standard BST descent from that node
        parent = None
        while current.is_real_node():
            parent = current
            if key < current.key:
                if not current.left.is_real_node():
                    break
                current = current.left
            else:  # key > current.key
                if not current.right.is_real_node():
                    break
                current = current.right

        # Create and attach new node
        new_node = AVLNode(key, val)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Update max if needed
        if key > self.max.key:
            self.max = new_node

        self._size += 1
        self._balanced_nodes += 1
        return self.rebalance_after_change(new_node)

    def create_root(self, key: int, val: str) -> None:
        self.root = AVLNode(key, val)
        self.max = self.root
        self._size = 1
        self._balanced_nodes = 1

    # --- Deletion Methods ---
    def delete(self, node: Optional[AVLNode]) -> int:
        if node is None or not node.is_real_node():
            return 0

        if node.left.is_real_node() and node.right.is_real_node():
            succ = min_node_of(node.right)
            self._replace_node_data_with_successor(node, succ)
            node = succ

        if node == self.max:
            self._update_max_on_delete()

        child = self.get_least_none_child(node)

        self.switch_node_with(node, child)
        self._size -= 1
        if node.is_balanced:
            self._balanced_nodes -= 1

        rebalance_count = self.rebalance_after_change(child)

        if self._size == 0:
            self.root = VirtualAVLNode.get_create_instance()
            self.max = self.root

        return rebalance_count

    def get_least_none_child(self, node: AVLNode) -> AVLNode:
        child = node.left if node.left.is_real_node() else node.right
        return child

    def _replace_node_data_with_successor(self, node: AVLNode, succ: AVLNode) -> None:
        node.key, node.value = succ.key, succ.value

    def _update_max_on_delete(self) -> None:
        if self.max.left.is_real_node():
            self.max = self.max.left
        elif self.max.parent is not None:
            self.max = self.max.parent
        else:
            self.max = VirtualAVLNode.get_create_instance()

    # --- Traversal Methods ---
    def avl_to_array(self) -> List[Tuple[int, str]]:
        result: List[Tuple[int, str]] = []
        self.inorder_collect(self.root, result)
        return result

    def inorder_collect(self, node: Optional[AVLNode], result: List[Tuple[int, str]]) -> None:
        if node is None or not node.is_real_node():
            return
        self.inorder_collect(node.left, result)
        result.append((node.key, node.value))
        self.inorder_collect(node.right, result)

    # --- Size/Root/Balance Methods ---
    def size(self) -> int:
        return self._size

    def get_root(self) -> Optional[AVLNode]:
        if self.root.is_real_node():
            return self.root
        return None

    def get_amir_balance_factor(self) -> float:
        return self._balanced_nodes / self._size if self._size > 0 else 0

    # --- Rebalancing Methods ---
    def rebalance_after_change(self, changed_node: AVLNode) -> int:
        rebalance_count = 0
        node = changed_node.parent
        while node is not None:
            old_height = node.height
            self.update_node_data(node)
            balance = self.get_balance(node)
            if abs(balance) > 1:
                rebalance_count += self.rebalance_node(node)
                node = node.parent
            else:
                rebalance_count += 1
            if node.height == old_height:
                break
            node = node.parent
        return rebalance_count

    def update_node_data(self, node: AVLNode) -> None:
        node.height = 1 + max(node.left.height, node.right.height)
        new_is_balanced = (node.left.height == node.right.height)
        if new_is_balanced != node.is_balanced:
            if new_is_balanced:
                self._balanced_nodes += 1
            else:
                self._balanced_nodes -= 1
        node.is_balanced = new_is_balanced


    #prints tree fancily, useful for debugging
    def print_tree_fancily(self, file: Optional[str] = None, append: bool = True, bykey: bool = True) -> None:
        printree(self.root, file=file, append=append, bykey=bykey)

    def rebalance_node(self, node: AVLNode) -> int:
        rebalance_count = 0
        if self.get_balance(node) > 1:
            if self.get_balance(node.left) < 0:
                self.rotate_left(node.left)
                rebalance_count += 1
            self.rotate_right(node)
        elif self.get_balance(node) < -1:
            if self.get_balance(node.right) > 0:
                self.rotate_right(node.right)
                rebalance_count += 1
            self.rotate_left(node)
        return rebalance_count + 1

    def rotate_left(self, x: AVLNode) -> None:
        y = x.right
        x.right = y.left
        if y.left.is_real_node():
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y
        self.update_node_data(x)
        self.update_node_data(y)

    def rotate_right(self, y: AVLNode) -> None:
        x = y.left
        y.left = x.right
        if x.right.is_real_node():
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        else:
            if y == y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x
        x.right = y
        y.parent = x
        self.update_node_data(y)
        self.update_node_data(x)

    def switch_node_with(self, node: AVLNode, child: AVLNode) -> None:
        if node.parent is None:
            self.root = child
            child.parent = None
        else:
            if node == node.parent.left:
                node.parent.left = child
            else:
                node.parent.right = child
            child.parent = node.parent

    def get_max_node(self) -> AVLNode:
        return self.max
    
    def get_balance(self, node: AVLNode) -> int:
        return node.get_bf()
    
    def _get_balance(self, node: AVLNode) -> int:
        return node.get_bf()
    



# =============================
# End of AVL Tree Implementation
# =============================


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