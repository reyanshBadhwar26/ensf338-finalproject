class AVLNode:
    def __init__(self, booking):
        self.booking = booking
        self.key = (booking.event_date, booking.start_time, booking.room)

        self.left = None
        self.right = None
        self.balance = 0


class BookingAVLTree:

    def __init__(self):
        self.root = None

    def insert(self, booking):
        if self.root is None:
            self.root = AVLNode(booking)
            return

        current = self.root
        path = []

        key = (booking.event_date, booking.start_time, booking.room)

        # Step 1: normal BST insert
        while True:
            path.append(current)

            if key <= current.key:
                if current.left is None:
                    current.left = AVLNode(booking)
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = AVLNode(booking)
                    break
                current = current.right

        # Step 2: find pivot
        pivot = None
        for node in reversed(path):
            if node.balance != 0:
                pivot = node
                break

        pivot_index = path.index(pivot) if pivot is not None else -1

        # CASE 1
        if pivot is None:
            print("Case 1: No pivot")

            for node in path:
                if key <= node.key:
                    node.balance -= 1
                else:
                    node.balance += 1

        else:
            # CASE 2
            if (pivot.balance == -1 and key > pivot.key) or \
               (pivot.balance == 1 and key < pivot.key):

                print("Case 2: Inserted into shorter subtree")

                for node in path[:pivot_index + 1]:
                    if key <= node.key:
                        node.balance -= 1
                    else:
                        node.balance += 1

            # CASE 3a (outside)
            elif (pivot.balance == -1 and key <= pivot.left.key) or \
                 (pivot.balance == 1 and key > pivot.right.key):

                print("Case 3a: Outside rotation")

                for node in path[pivot_index + 1:]:
                    if key <= node.key:
                        node.balance -= 1
                    else:
                        node.balance += 1

                if key <= pivot.key:
                    pivot.balance -= 1
                    new_root = self._right_rotate(pivot)
                else:
                    pivot.balance += 1
                    new_root = self._left_rotate(pivot)

                self._reconnect(path, pivot_index, pivot, new_root)

            # CASE 3b (inside)
            else:
                print("Case 3b: Inside rotation")

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


    def delete(self, event_date, start_time, room):
        key = (event_date, start_time, room)
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)

        elif key > node.key:
            node.right = self._delete(node.right, key)

        else:
            if node.left is None:
                return node.right

            if node.right is None:
                return node.left

            temp = self._get_min(node.right)
            node.key = temp.key
            node.booking = temp.booking
            node.right = self._delete(node.right, temp.key)

        return self._rebalance(node)

    def _get_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _rebalance(self, node):
        self._update_balance(node)

        if node.balance < -1:
            if node.left.balance <= 0:
                return self._right_rotate(node)
            else:
                return self._lr_rotate(node)

        if node.balance > 1:
            if node.right.balance >= 0:
                return self._left_rotate(node)
            else:
                return self._rl_rotate(node)

        return node

    def _update_balance(self, node):
        node.balance = self._height(node.right) - self._height(node.left)

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def _left_rotate(self, node):
        right_child = node.right
        node.right = right_child.left
        right_child.left = node

        node.balance = node.balance - 1 - max(0, right_child.balance)
        right_child.balance = right_child.balance - 1 + min(0, node.balance)

        return right_child


    def _right_rotate(self, node):
        left_child = node.left
        node.left = left_child.right
        left_child.right = node

        node.balance = node.balance + 1 - min(0, left_child.balance)
        left_child.balance = left_child.balance + 1 + max(0, node.balance)

        return left_child


    def _lr_rotate(self, node):
        node.left = self._left_rotate(node.left)
        return self._right_rotate(node)


    def _rl_rotate(self, node):
        node.right = self._right_rotate(node.right)
        return self._left_rotate(node)

    def _reconnect(self, path, pivot_index, pivot, new_root):
        if pivot_index == 0:
            self.root = new_root
        else:
            parent = path[pivot_index - 1]
            if parent.left == pivot:
                parent.left = new_root
            else:
                parent.right = new_root

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

    def print_tree(self):
        if self.root is None:
            print("Empty tree.")
        else:
            self._print_tree(self.root, 0, "Root: ")

    def _print_tree(self, node, level, label):
        if node is None:
            return

        self._print_tree(node.right, level + 1, "R--- ")
        real_balance = self._height(node.right) - self._height(node.left)
        print("    " * level + label + f"{node.booking.event_name} ({node.booking.start_time}) (b={real_balance})")
        self._print_tree(node.left, level + 1, "L--- ")