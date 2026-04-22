# Node class for AVL tree
# Each node stores a booking and a key used for ordering
class AVLNode:
    def __init__(self, booking):
        self.booking = booking
        
        # Key is a tuple so we can compare bookings easily
        # Ordered by date then time then room
        self.key = (booking.event_date, booking.start_time, booking.room)

        self.left = None   # left child
        self.right = None  # right child
        self.balance = 0   # balance factor (right height - left height)


# BONUS - AVL Tree to store bookings
# Keeps tree balanced for efficient search, insert, delete (O(log n))
class BookingAVLTree:

    def __init__(self):
        self.root = None  # start with empty tree

    def insert(self, booking):
        # If tree empty → insert directly
        if self.root is None:
            self.root = AVLNode(booking)
            return

        current = self.root
        path = []  # track nodes visited (used later for balancing)

        key = (booking.event_date, booking.start_time, booking.room)

        # STEP 1: Normal BST insert
        while True:
            path.append(current)

            if key <= current.key:
                # go left
                if current.left is None:
                    current.left = AVLNode(booking)
                    break
                current = current.left
            else:
                # go right
                if current.right is None:
                    current.right = AVLNode(booking)
                    break
                current = current.right

        # STEP 2: Find pivot (first node that is already unbalanced)
        pivot = None
        for node in reversed(path):
            if node.balance != 0:
                pivot = node
                break

        pivot_index = path.index(pivot) if pivot is not None else -1

        # CASE 1: No pivot - update balances
        if pivot is None:
            for node in path:
                if key <= node.key:
                    node.balance -= 1
                else:
                    node.balance += 1

        else:
            # CASE 2: Pivot becomes balanced again (no rotation needed)
            if (pivot.balance == -1 and key > pivot.key) or \
               (pivot.balance == 1 and key < pivot.key):

                for node in path[:pivot_index + 1]:
                    if key <= node.key:
                        node.balance -= 1
                    else:
                        node.balance += 1

            # CASE 3a: Outside case - single rotation (LL or RR)
            elif (pivot.balance == -1 and key <= pivot.left.key) or \
                 (pivot.balance == 1 and key > pivot.right.key):

                # update balances below pivot
                for node in path[pivot_index + 1:]:
                    if key <= node.key:
                        node.balance -= 1
                    else:
                        node.balance += 1

                # perform rotation
                if key <= pivot.key:
                    pivot.balance -= 1
                    new_root = self._right_rotate(pivot)
                else:
                    pivot.balance += 1
                    new_root = self._left_rotate(pivot)

                # reconnect rotated subtree
                self._reconnect(path, pivot_index, pivot, new_root)

            # CASE 3b: Inside case - double rotation (LR or RL)
            else:
                for node in path[pivot_index + 1:]:
                    if key <= node.key:
                        node.balance -= 1
                    else:
                        node.balance += 1

                if pivot.balance == -1:
                    pivot.balance -= 1
                    new_root = self._lr_rotate(pivot)
                else:
                    pivot.balance += 1
                    new_root = self._rl_rotate(pivot)

                self._reconnect(path, pivot_index, pivot, new_root)

    # delete function
    def delete(self, event_date, start_time, room):
        key = (event_date, start_time, room)
        self.root = self._delete(self.root, key)

    # Recursive delete helper
    def _delete(self, node, key):
        if node is None:
            return None

        # Traverse tree like BST
        if key < node.key:
            node.left = self._delete(node.left, key)

        elif key > node.key:
            node.right = self._delete(node.right, key)

        else:
            # Node found → handle cases

            # Case: one child or no child
            if node.left is None:
                return node.right

            if node.right is None:
                return node.left

            # Case: two children → replace with inorder successor
            temp = self._get_min(node.right)
            node.key = temp.key
            node.booking = temp.booking
            node.right = self._delete(node.right, temp.key)

        # Rebalance after deletion
        return self._rebalance(node)

    # Get smallest node in subtree (leftmost)
    def _get_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # Rebalance node if needed
    def _rebalance(self, node):
        self._update_balance(node)

        # Left heavy
        if node.balance < -1:
            if node.left.balance <= 0:
                return self._right_rotate(node)
            else:
                return self._lr_rotate(node)

        # Right heavy
        if node.balance > 1:
            if node.right.balance >= 0:
                return self._left_rotate(node)
            else:
                return self._rl_rotate(node)

        return node

    # Update balance factor using subtree heights
    def _update_balance(self, node):
        node.balance = self._height(node.right) - self._height(node.left)

    # Compute height recursively
    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    #This function checks if the tree is balanced by verifying the balance factor of each node
    def check(self, node):
        if node is None:
            return True
        balance = self._height(node.right) - self._height(node.left)
        if abs(balance) > 1:
            return False
        return self.check(node.left) and self.check(node.right)
    
    def is_balanced(self):
        return self.check(self.root)
    
    # Left rotation (RR case)
    def _left_rotate(self, node):
        right_child = node.right
        node.right = right_child.left
        right_child.left = node

        # update balances
        node.balance = node.balance - 1 - max(0, right_child.balance)
        right_child.balance = right_child.balance - 1 + min(0, node.balance)

        return right_child

    # Right rotation (LL case)
    def _right_rotate(self, node):
        left_child = node.left
        node.left = left_child.right
        left_child.right = node

        node.balance = node.balance + 1 - min(0, left_child.balance)
        left_child.balance = left_child.balance + 1 + max(0, node.balance)

        return left_child

    # Left-Right rotation
    def _lr_rotate(self, node):
        node.left = self._left_rotate(node.left)
        return self._right_rotate(node)

    # Right-Left rotation
    def _rl_rotate(self, node):
        node.right = self._right_rotate(node.right)
        return self._left_rotate(node)

    # Reconnect rotated subtree to parent
    def _reconnect(self, path, pivot_index, pivot, new_root):
        if pivot_index == 0:
            self.root = new_root
        else:
            parent = path[pivot_index - 1]
            if parent.left == pivot:
                parent.left = new_root
            else:
                parent.right = new_root

    # Search for a booking by key
    def search(self, event_date, start_time, room):
        key = (event_date, start_time, room)
        current = self.root

        while current is not None:
            if key == current.key:
                return current.booking
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        return None

    # Print tree structure to show that it remains balanced 
    def print_tree(self):
        if self.root is None:
            print("Empty tree.")
        else:
            self._print_tree(self.root, 0, "Root: ")

    # Recursive print helper
    def _print_tree(self, node, level, label):
        if node is None:
            return

        self._print_tree(node.right, level + 1, "R--- ")
        real_balance = self._height(node.right) - self._height(node.left)
        print("    " * level + label + f"{node.booking.event_name} ({node.booking.start_time}) (b={real_balance})")
        self._print_tree(node.left, level + 1, "L--- ")