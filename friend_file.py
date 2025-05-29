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

    def __init__(self, key, value, isVirtual=False):
        self.key = key
        self.value = value
        self.parent = None
        self.left = None if isVirtual else AVLNodeVirtual.instance()
        self.right = None if isVirtual else AVLNodeVirtual.instance()
        self.height = 0 if not isVirtual else -1
        self.isBalanced = True if not isVirtual else False

    """returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""

    def is_real_node(self):
        return True

    def __str__(self):
        if not self.is_real_node():
            return "#"

        return f"({self.key}, {self.value})"
    
    def get_bf(self):
        return self.left.height - self.right.height


class AVLNodeVirtual(AVLNode):
    __instance = None

    def __init__(self):
        super().__init__(None, None, True)

    @staticmethod
    def instance():
        if AVLNodeVirtual.__instance is None:
            AVLNodeVirtual.__instance = AVLNodeVirtual()
        return AVLNodeVirtual.__instance

    def is_real_node(self):
        return False


"""
A class implementing an AVL tree.
"""


def get_balance(node):
    return node.left.height - node.right.height


def _min_node(node):
    while node.left.is_real_node():
        node = node.left
    return node


class AVLTree(object):
    """
	Constructor, you are allowed to add more fields.

	"""

    def __init__(self):
        self.root = AVLNodeVirtual.instance()
        self.max = self.root
        self._size = 0
        self._balanced_nodes = 0

    """searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""

    def search(self, key):
        node = self.root
        while node.is_real_node():
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    """inserts a new node into the dictionary with corresponding key and value

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@param start: can be either "root" or "max"
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

    def insert(self, key, val, start="root"):
        if not self.root.is_real_node():
            self.root = AVLNode(key, val)
            self.max = self.root
            self._size = 1
            self._balanced_nodes = 1
            return 0

        if start == "max":
            node = self.max
            while node != self.root and node.key > key:
                node = node.parent
        else:
            node = self.root

        parent = None
        while node.is_real_node():
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        new_node = AVLNode(key, val)
        new_node.parent = parent

        if key > self.max.key:
            self.max = new_node

        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._size += 1
        self._balanced_nodes += 1
        return self.rebalance_after_change(new_node)

    """deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

    def delete(self, node):
        if node is None or not node.is_real_node():
            return 0

        if node.left.is_real_node() and node.right.is_real_node():
            succ = _min_node(node.right)
            node.key, node.value = succ.key, succ.value
            node = succ

        if node == self.max:
            if self.max.left.is_real_node():
                self.max = self.max.left
            elif self.max.parent is not None:
                self.max = self.max.parent
            else:
                self.max = AVLNodeVirtual.instance()

        child = node.left if node.left.is_real_node() else node.right

        self.replace_node(node, child)
        self._size -= 1
        if node.isBalanced:
            self._balanced_nodes -= 1

        rebalance_count = self.rebalance_after_change(child)

        if self._size == 0:
            self.root = AVLNodeVirtual.instance()
            self.max = self.root

        return rebalance_count

    """returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""

    def avl_to_array(self):
        res = []
        self.inorder(self.root, res)
        return res

    def inorder(self, node, res):
        if not node.is_real_node():
            return
        self.inorder(node.left, res)
        res.append((node.key, node.value))
        self.inorder(node.right, res)

    """returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""

    def size(self):
        return self._size

    """returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""

    def get_root(self):
        if self.root.is_real_node():
            return self.root
        return None

    """gets amir's suggestion of balance factor
	@returns: the number of nodes which have balance factor equals to 0 devided by the total number of nodes
	"""

    def get_amir_balance_factor(self):
        return self._balanced_nodes / self._size if self._size > 0 else 0

    def rebalance_after_change(self, changed_node):
        rebalance_count = 0
        node = changed_node.parent
        while node is not None:
            old_height = node.height
            self.update_node_fields(node)
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

    def update_node_fields(self, node):
        node.height = 1 + max(node.left.height, node.right.height)

        new_is_balanced = (node.left.height == node.right.height)
        if new_is_balanced != node.isBalanced:
            if new_is_balanced:
                self._balanced_nodes += 1
            else:
                self._balanced_nodes -= 1
        node.isBalanced = new_is_balanced

    def rebalance_node(self, node):
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

    def rotate_left(self, x):
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
        self.update_node_fields(x)
        self.update_node_fields(y)

    def rotate_right(self, y):
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
        self.update_node_fields(y)
        self.update_node_fields(x)

    def replace_node(self, node, child):
        if node.parent is None:
            self.root = child
            child.parent = None
        else:
            if node == node.parent.left:
                node.parent.left = child
            else:
                node.parent.right = child
            child.parent = node.parent

    def get_max_node(self):
        return self.max
    
    def get_balance(self, node :AVLNode):
        return node.get_bf()
    
    def _get_balance(self, node: AVLNode):
        return node.get_bf()


if __name__ == "__main__":
    avl_tree = AVLTree()
    avl_tree.insert(35, '35')
    avl_tree.insert(67, '67')
    avl_tree.insert(42, '42')
    avl_tree.insert(30, '30')
    avl_tree.insert(37, '37')
    avl_tree.insert(69, '69')
    avl_tree.insert(10, '10')
    avl_tree.insert(39, '39')
    avl_tree.insert(45, '45')
    avl_tree.insert(21, '21')
    avl_tree.insert(5, '5')
    avl_tree.insert(23, '23')
    avl_tree.insert(36, '36')
    avl_tree.insert(41, '41')
    avl_tree.insert(71, '71')
    avl_tree.insert(47, '47')
    avl_tree.insert(32, '32')
    avl_tree.insert(17, '17')
    avl_tree.insert(33, '33')
    avl_tree.insert(9, '9')
    avl_tree.insert(68, '68')
    avl_tree.insert(52, '52')
    avl_tree.insert(53, '53')
    avl_tree.insert(54, '54')
    avl_tree.insert(15, '15')
    avl_tree.insert(40, '40')
    x = 0
