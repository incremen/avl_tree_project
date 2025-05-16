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
    def __init__(self, key, value):
        self.key :int = key
        self.value = value
        self.left :AVLNode= None
        self.right :AVLNode= None
        self.parent :AVLNode= None
        self.height :int = -1
		

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """
    def is_real_node(self):
        return self.key is not None



"""
A class implementing an AVL tree.its
"""

class AVLTree(object):

    """
    Constructor, you are allowed to add more fields.  

    """
    def __init__(self):
        self.root = None
        self.node_count = 0


    """Returns the height of a node, or -1 if the node is not real.

    @type node: AVLNode
    @rtype: int
    @returns: height of the node if real, -1 otherwise
    """
    def height(self, node):
        if node is None or not node.is_real_node():
            return -1
        return node.height


    """Updates the height of a given node based on its children.

    @type node: AVLNode
    @pre: node is a real node
    @post: node.height is correctly updated to max(left, right) + 1
    @rtype: None
    """
    def update_height(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))


    """Computes the balance factor of a given node.

    @type node: AVLNode
    @rtype: int
    @returns: height(left child) - height(right child)
    """
    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right)


    """Performs a left rotation on the given node.

    @type node: AVLNode
    @pre: node.right is a real node
    @rtype: AVLNode
    @returns: new root of the subtree after rotation
    """
    def rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        if new_root.left:
            new_root.left.parent = node
        new_root.left = node
        new_root.parent = node.parent
        node.parent = new_root
        if new_root.parent is None:
            self.root = new_root
        elif new_root.parent.left == node:
            new_root.parent.left = new_root
        else:
            new_root.parent.right = new_root
        self.update_height(node)
        self.update_height(new_root)
        return new_root


    """Performs a right rotation on the given node.

    @type node: AVLNode
    @pre: node.left is a real node
    @rtype: AVLNode
    @returns: new root of the subtree after rotation
    """
    def rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        if new_root.right:
            new_root.right.parent = node
        new_root.right = node
        new_root.parent = node.parent
        node.parent = new_root
        if new_root.parent is None:
            self.root = new_root
        elif new_root.parent.right == node:
            new_root.parent.right = new_root
        else:
            new_root.parent.left = new_root
        self.update_height(node)
        self.update_height(new_root)
        return new_root


    """Rebalances the tree starting from the given node upwards to the root.

    @type node: AVLNode
    @pre: node is a real node in the tree
    @rtype: int
    @returns: number of rotations performed
    """
    def rebalance(self, node):
        rotations = 0
        while node:
            self.update_height(node)
            bf = self.balance_factor(node)
            if bf > 1:
                if self.balance_factor(node.left) < 0:
                    node.left = self.rotate_left(node.left)
                    rotations += 1
                node = self.rotate_right(node)
                rotations += 1
            elif bf < -1:
                if self.balance_factor(node.right) > 0:
                    node.right = self.rotate_right(node.right)
                    rotations += 1
                node = self.rotate_left(node)
                rotations += 1
            if node.parent is None:
                self.root = node
            node = node.parent
        return rotations


    """replaces the subtree rooted at node u with the subtree rooted at node v

    @type u: AVLNode
    @param u: the node to be replaced
    @type v: AVLNode | None
    @param v: the node to replace u with (can be None)
    @rtype: None
    @return: None
    """
    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent


    """returns the node with the minimum key in the subtree rooted at the given node

    @type node: AVLNode
    @param node: the root of the subtree
    @rtype: AVLNode
    @return: the node with the minimum key in the subtree
    """
    def min_node(self, node):
        while node.left is not None:
            node = node.left
        return node


    """Traverses the tree rooted at 'node' in in-order and appends (key, value) pairs to 'result'.

    @type node: AVLNode
    @param node: root of the current subtree
    @type result: list
    @param result: list to which (key, value) pairs will be appended
    @rtype: None
    @return: None
    """
    def inorder_collect(self, node, result):
        if node is None or not node.is_real_node():
            return
        self.inorder_collect(node.left, result)
        result.append((node.key, node.value))
        self.inorder_collect(node.right, result)


    """Recursively counts how many real nodes in the subtree rooted at 'node' have a balance factor of exactly 0.

    @type node: AVLNode
    @param node: root of the subtree
    @rtype: int
    @return: number of real nodes with balance factor 0
    """
    def count_zero_balance_nodes(self, node):
        if node is None or not node.is_real_node():
            return 0
        left = self.count_zero_balance_nodes(node.left)
        right = self.count_zero_balance_nodes(node.right)
        bf = self.balance_factor(node)
        return left + right + (1 if bf == 0 else 0)

    
    """searches for a node in the dictionary corresponding to the key

    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: node corresponding to key
    """
    def search(self, key):
        node = self.root
        while node:
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
        if self.root is None:
            self.root = AVLNode(key, val)
            self.root.height = 0
            self.node_count += 1
            return 0
        if start == "root":
            current = self.root
        else:
            current = self.root
            while current.right and current.right.is_real_node():
                current = current.right
        parent = None
        while current:
            parent = current
            if key < current.key:
                if current.left is None or not current.left.is_real_node():
                    break
                current = current.left
            else:
                if current.right is None or not current.right.is_real_node():
                    break
                current = current.right
        new_node = AVLNode(key, val)
        new_node.height = 0
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self.node_count += 1
        return self.rebalance(parent)


    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
    def delete(self, node):
        if node.left is None:
            self.transplant(node, node.right)
            rebalance_start = node.parent
        elif node.right is None:
            self.transplant(node, node.left)
            rebalance_start = node.parent
        else:
            successor = self.min_node(node.right)
            if successor.parent != node:
                self.transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor
            self.transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor
            rebalance_start = successor
        node.left = None
        node.right = None
        node.parent = None
        self.node_count -= 1
        return self.rebalance(rebalance_start)


    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """
    def avl_to_array(self):
        result = []
        self.inorder_collect(self.root, result)
        return result


    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    def size(self):
        return self.node_count	


    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        return self.root


    """gets amir's suggestion of balance factor

	@returns: the number of nodes which have balance factor equals to 0 devided by the total number of nodes
	"""
    def get_amir_balance_factor(self):
        if self.node_count == 0:
            return 0.0  
        count = self.count_zero_balance_nodes(self.root)
        return count / self.node_count
