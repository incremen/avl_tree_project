class BSTNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

class BSTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.max_node = None  # Pointer to the maximum node

    def insert(self, key, val, start="root"):
        node = BSTNode(key, val)
        if self.root is None:
            self.root = node
            self.max_node = node
            self.size += 1
            return

        if start == "root":
            current = self.root
        elif start == "max":
            current = self.max_node  # Start from the maximum node
        else:
            raise ValueError("Invalid start value")

        while True:
            if key < current.key:
                if current.left is None:
                    current.left = node
                    node.parent = current
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = node
                    node.parent = current
                    break
                current = current.right

        # Update max_node if needed
        if self.max_node is None or key > self.max_node.key:
            self.max_node = node

        self.size += 1
