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
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.zero_balance_count = 0  # Number of nodes in subtree with balance factor 0
		

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.key is not None

	def get_height(self):
		if not self.is_real_node():
			return -1
		return self.height

	def balance_factor(self):
		left_height = self.left.get_height() if self.left else -1
		right_height = self.right.get_height() if self.right else -1
		return left_height - right_height

	def update_stats(self):
		"""Update height and zero_balance_count for this node."""
		left_height = self.left.get_height() if self.left else -1
		right_height = self.right.get_height() if self.right else -1
		self.height = 1 + max(left_height, right_height)
		left_zb = self.left.zero_balance_count if self.left and self.left.is_real_node() else 0
		right_zb = self.right.zero_balance_count if self.right and self.right.is_real_node() else 0
		self.zero_balance_count = left_zb + right_zb + (1 if self.balance_factor() == 0 else 0)



"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.root = None


	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""
	def search(self, key):
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
		# Find the correct parent for the new node
		parent = None
		current = self.root
		while current:
			parent = current
			if key < current.key:
				if current.left is None:
					break
				current = current.left
			else:
				if current.right is None:
					break
				current = current.right
		new_node = AVLNode(key, val)
		new_node.parent = parent
		if parent is None:
			self.root = new_node
		elif key < parent.key:
			parent.left = new_node
		else:
			parent.right = new_node
		self.update_upwards(parent)
		return 0  # or the number of rebalancing operations if you implement AVL balancing


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		if node is None:
			return 0
		if node.left is None:
			self._transplant(node, node.right)
			rebalance_start = node.parent
		elif node.right is None:
			self._transplant(node, node.left)
			rebalance_start = node.parent
		else:
			successor = node.right
			while successor.left:
				successor = successor.left
			if successor.parent != node:
				self._transplant(successor, successor.right)
				successor.right = node.right
				if successor.right:
					successor.right.parent = successor
			self._transplant(node, successor)
			successor.left = node.left
			if successor.left:
				successor.left.parent = successor
			rebalance_start = successor
		self.update_upwards(rebalance_start)
		return 0  # or the number of rebalancing operations if you implement AVL balancing


	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		return None


	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return -1	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return None


	"""gets amir's suggestion of balance factor

	@returns: the number of nodes which have balance factor equals to 0 devided by the total number of nodes
	"""
	def get_amir_balance_factor(self):
		return None

	def update_upwards(self, node):
		"""Update height and zero_balance_count from node up to root."""
		while node:
			node.update_stats()
			node = node.parent

	def _transplant(self, u, v):
		if u.parent is None:
			self.root = v
		elif u == u.parent.left:
			u.parent.left = v
		else:
			u.parent.right = v
		if v:
			v.parent = u.parent