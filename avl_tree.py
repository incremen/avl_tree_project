def rotate_left(tree, node):
    new_parent = node.right
    node.right = new_parent.left
    if new_parent.left:
        new_parent.left.parent = node
    new_parent.left = node
    new_parent.parent = node.parent
    node.parent = new_parent
    if new_parent.parent is None:
        tree.root = new_parent
    elif new_parent.parent.left == node:
        new_parent.parent.left = new_parent
    else:
        new_parent.parent.right = new_parent
    node.update_stats()
    new_parent.update_stats()
    return


def rotate_right(tree, node):
    new_parent = node.left
    node.left = new_parent.right
    if new_parent.right:
        new_parent.right.parent = node
    new_parent.right = node
    new_parent.parent = node.parent
    node.parent = new_parent
    if new_parent.parent is None:
        tree.root = new_parent
    elif new_parent.parent.right == node:
        new_parent.parent.right = new_parent
    else:
        new_parent.parent.left = new_parent
    node.update_stats()
    new_parent.update_stats()
    return 


def update_and_rebalance_upwards(tree, node, called_from_insert):
    """Update stats and rebalance the tree starting from the given node upwards to the root.

    @type tree: AVLTree
    @type node: AVLNode
    @type called_from_insert: bool
    @rtype: int
    @returns: number of rotations performed
    """
    rotations = 0
    while node:
        old_height = node.height
        node.update_stats()
        bf = node.balance_factor()

        # Perform rotations if needed
        if bf > 1:
            if node.left.balance_factor() < 0:
                rotate_left(tree, node.left)
                rotations += 1
            rotate_right(tree, node)
            rotations += 1
            if called_from_insert:
                break
        elif bf < -1:
            if node.right.balance_factor() > 0:
                rotate_right(tree, node.right)
                rotations += 1
            rotate_left(tree, node)
            rotations += 1
            if called_from_insert:
                break

        if node.height == old_height:
            break

        # Update root if necessary
        if node.parent is None:
            tree.root = node

        node = node.parent

    return rotations


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

    def update_stats(self):
        left_height = self.left.get_height() if self.left else -1
        right_height = self.right.get_height() if self.right else -1
        self.height = 1 + max(left_height, right_height)


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
        self.max_node = None  
        self.total_zero_balance_nodes = 0


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


    """Rebalances the tree starting from the given node upwards to the root.

    @type node: AVLNode
    @pre: node is a real node in the tree
    @rtype: int
    @returns: number of rotations performed
    """

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
        return node
    

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent


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
        """Insert a node with key and val. Use 'root' or 'max' as a starting point.
        @type key: int
        @type val: str
        @rtype: int
        @returns: number of AVL rebalancing operations
        """
        # Handle empty tree case
        if self.root is None:
            self.root = AVLNode(key, val)
            self.root.height = 0
            self.max_node = self.root
            self.node_count += 1
            return 0

        # Choose starting point
        current = self.root if start == "root" else self.max_node

        # If starting from max, climb UP until we're at a node whose subtree should contain the new key
        if start == "max":
            while current.key > key and current.parent:
                current = current.parent

                
        # Now do standard BST descent from that node
        parent = None
        while current:
            parent = current
            if key < current.key:
                if current.left is None or not current.left.is_real_node():
                    break
                current = current.left
            else:  # key > current.key
                if current.right is None or not current.right.is_real_node():
                    break
                current = current.right

        # Create and attach new node
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

        # Update metadata and rebalance
        new_node.update_stats()
        self.node_count += 1
        return update_and_rebalance_upwards(self, parent, True)


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
        self.node_count -= 1
        return update_and_rebalance_upwards(self, rebalance_start, False)

    def min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

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
        return None

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
    
    def get_max_node(self):
        """returns the maximum node in the tree

        @rtype: AVLNode
        @returns: the node with the maximum key, None if the tree is empty
        """
        return self.max_node
