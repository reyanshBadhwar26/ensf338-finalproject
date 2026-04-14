class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.size = 0
        self.front = None
        self.rear = None

    def is_empty(self):
        return self.size == 0
    def peek(self):
        if self.is_empty():
            return None
        return self.front.data

    def enqueue(self, item):
        new_node = Node(item)
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size = self.size + 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("The queue is empty")
        item = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size = self.size - 1
        return item
    
    def __len__(self):
        return self.size
    
    def to_list(self):
        items = []
        current = self.front
        while current is not None:
            items.append(current.data)
            current = current.next
        return items
    