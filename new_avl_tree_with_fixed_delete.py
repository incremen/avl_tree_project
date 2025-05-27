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
        self.zero_balance_count :int = 0


		

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """
    def is_real_node(self):
        return self.key is not None

    """Returns the height of a node, or -1 if the node is not real.

    @rtype: int
    @returns: height of the node if real, -1 otherwise
    """
    def get_height(self):
        if self is None or not self.is_real_node():
            return -1
        return self.height

    def get_bf(self):
        left_height = self.left.get_height() if self.left else -1
        right_height = self.right.get_height() if self.right else -1
        return left_height - right_height
    
    def balance_factor(self):
        return self.get_bf()

    """Update height and zero_balance_count for this node."""
    def update_stats(self):
        left_height = self.left.get_height() if self.left else -1
        right_height = self.right.get_height() if self.right else -1
        self.height = 1 + max(left_height, right_height)
        left_zb = self.left.zero_balance_count if self.left and self.left.is_real_node() else 0
        right_zb = self.right.zero_balance_count if self.right and self.right.is_real_node() else 0
        self.zero_balance_count = left_zb + right_zb + (1 if self.get_bf() == 0 else 0)


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
        self.max_node = None  # Maintain a pointer to the maximum node


    """Updates the height of a given node based on its children.

    @type node: AVLNode
    @pre: node is a real node
    @post: node.height is correctly updated to max(left, right) + 1
    @rtype: None
    """
    def update_height(self, node):
        node.height = 1 + max(node.left.get_height() if node.left else -1, node.right.get_height() if node.right else -1)


    """Computes the balance factor of a given node.

    @type node: AVLNode
    @rtype: int
    @returns: height(left child) - height(right child)
    """
    def get_bf(self, node):
        return (node.left.get_height() if node.left else -1) - (node.right.get_height() if node.right else -1)


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
        node.update_stats()
        new_root.update_stats()
        self.update_upwards(new_root.parent)
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
        node.update_stats()
        new_root.update_stats()
        self.update_upwards(new_root.parent)
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
            old_height = node.height
            node.update_stats()
            bf = node.balance_factor()
            if bf > 1:
                if node.left.balance_factor() < 0:
                    node.left = self.rotate_left(node.left)
                    rotations += 1
                node = self.rotate_right(node)
                rotations += 1
            elif bf < -1:
                if node.right.balance_factor() > 0:
                    node.right = self.rotate_right(node.right)
                    rotations += 1
                node = self.rotate_left(node)
                rotations += 1

            # If height hasn't changed after rebalancing, we can stop
            if node.height == old_height:
                break
                
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
        bf = self.get_bf(node)
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
            self.max_node = self.root  # Set max_node to root
            self.node_count += 1
            return 0
        if start == "root":
            current = self.root
        elif start == "max":
            current = self.max_node  # Use the max_node pointer
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
        # Update max_node if needed
        if self.max_node is None or key > self.max_node.key:
            self.max_node = new_node
        new_node.update_stats()  # Ensure the new node's stats are set
        self.update_upwards(parent)
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
                if successor.right:
                    successor.right.parent = successor
                rebalance_start = successor.parent  # Start from successor's parent
            else:
                rebalance_start = successor  # Successor is direct child
            self.transplant(node, successor)
            successor.left = node.left
            if successor.left:
                successor.left.parent = successor
        node.left = None
        node.right = None
        node.parent = None
        # Update max_node if needed
        if self.max_node == node:
            # Find new max_node (rightmost node)
            curr = self.root
            prev = None
            while curr and curr.is_real_node() and curr.right:
                prev = curr
                curr = curr.right
            if curr and curr.is_real_node():
                self.max_node = curr
            else:
                self.max_node = prev
        self.update_upwards(rebalance_start)
        self.node_count -= 1
        return self.rebalance(rebalance_start)

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def rebalance(self, node):
        rotations = 0
        while node:
            old_height = node.height
            node.update_stats()
            bf = node.balance_factor()
            if bf > 1:
                if node.left.balance_factor() < 0:
                    node.left = self.rotate_left(node.left)
                    rotations += 1
                node = self.rotate_right(node)
                rotations += 1
            elif bf < -1:
                if node.right.balance_factor() > 0:
                    node.right = self.rotate_right(node.right)
                    rotations += 1
                node = self.rotate_left(node)
                rotations += 1
                
            if node.parent is None:
                self.root = node
            node = node.parent
        return rotations

    def update_upwards(self, node):
        """Update height and zero_balance_count from node up to root, stopping if height remains unchanged."""
        while node:
            old_height = node.height
            node.update_stats()
            if node.height == old_height:
                break  # Stop if height remains unchanged
            node = node.parent

    

    def _get_balance(self, node):
        return node.get_bf()
    

    def get_root(self):
        """returns the root of the tree representing the dictionary

        @rtype: AVLNode
        @returns: the root, None if the dictionary is empty
        """
        return self.root

    def get_amir_balance_factor(self):
        """gets amir's suggestion of balance factor

        @returns: the number of nodes which have balance factor equals to 0 divided by the total number of nodes
        """
        if self.node_count == 0:
            return 0.0
        return self.root.zero_balance_count / self.node_count

    def size(self):
        """returns the number of items in dictionary 

        @rtype: int
        @returns: the number of items in dictionary 
        """
        return self.node_count

    def avl_to_array(self):
        """returns an array representing dictionary 

        @rtype: list
        @returns: a sorted list according to key of tuples (key, value) representing the data structure
        """
        result = []
        self.inorder_collect(self.root, result)
        return result
