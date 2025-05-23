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

    def insert(self, key, val, start="root"):
        node = BSTNode(key, val)
        if self.root is None:
            self.root = node
            self.size += 1
            return

        if start == "root":
            current = self.root
        elif start == "max":
            current = self.root
            while current.right:
                current = current.right
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
        self.size += 1
