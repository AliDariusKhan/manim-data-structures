class Node:
    """Simple class that represents a BST node"""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.balance = 0
        self.parent = None

class BST:
    """Class that represents a full binary search tree"""
    def __init__(self):
        self.root = None
    
    def insert(self, keys):
        """Inserts a list of keys into the BST recursively"""
        def insert_helper(node, key):
            if node is None:
                return Node(key)
            if key < node.key:
                node.left = insert_helper(node.left, key)
                node.left.parent = node
            else:
                node.right = insert_helper(node.right, key)
                node.right.parent = node
            return node

        for key in keys:
            self.root = insert_helper(self.root, key)
    
    def __init__(self, keys=None):
        self.root = None
        if keys:
            self.insert(keys)
    
    def search(self, key):
        """Returns a list of nodes containing the path from root to target node"""
        path = []
        def search_helper(node, key):
            if node is None:
                return None
            path.append(node)
            if key < node.key:
                return search_helper(node.left, key)
            elif key > node.key:
                return search_helper(node.right, key)
            else:
                return node
        
        return search_helper(self.root, key), path[:-1]

    def delete(self, key):
        """Deletes the node with the given key from the tree"""
        parent, temp, is_left_child = None, self.root, False
        while temp.key != key:
            parent = temp
            if key < temp.key:
                is_left_child = True
                temp = temp.left
            else:
                temp = temp.right
        
        if temp.left is None and temp.right is None:
            if parent is None:
                self.root = None
                return
            if is_left_child:
                parent.left = None
            else:
                parent.right = None
        
        elif temp.left is None or temp.right is None:
            if parent is None:
                self.root = temp.left 
    
    def update_balances(self):
        """Updates the balance of all nodes in the tree"""
        def update_balances_helper(node):
            if node is None:
                return -1
            left_depth = 1 + update_balances_helper(node.left)
            right_depth = 1 + update_balances_helper(node.right)
            node.balance = right_depth - left_depth
            return max(left_depth, right_depth)
        
        update_balances_helper(self.root)
s