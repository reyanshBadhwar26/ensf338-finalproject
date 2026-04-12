
from service_request import ServiceRequest

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
    
class PriorityServiceQueue:
    def __init__(self):
        self.emergency_queue = Queue()
        self.standard_queue = Queue()
        self.low_queue = Queue()

    def add_request(self, request: ServiceRequest):
        if (request.priority == "Emergency"):
            self.emergency_queue.enqueue(request)
        elif (request.priority == "Standard"):
            self.standard_queue.enqueue(request)
        elif (request.priority == "Low"):
            self.low_queue.enqueue(request)
        else:
            raise ValueError("The priority type is invalid")
        


    def is_empty(self):
        return(self.emergency_queue.is_empty() and self.standard_queue.is_empty() and self.low_queue.is_empty())
        


    def total_requests(self):
        return (len(self.emergency_queue) + len(self.standard_queue) + len(self.low_queue))

    def serve_next_request(self):
        if not self.emergency_queue.is_empty():
            return self.emergency_queue.dequeue()
        if not self.standard_queue.is_empty():
            return self.standard_queue.dequeue()
        if not self.low_queue.is_empty():
            return self.low_queue.dequeue()
        return None
    
    def peek_next_request(self):
        if not self.emergency_queue.is_empty():
            return self.emergency_queue.peek()
        if not self.standard_queue.is_empty():
            return self.standard_queue.peek()
        if not self.low_queue.is_empty():
            return self.low_queue.peek()
        return None
    
        
    def display_queue(self):
        print("\nEmergency Queue: ")
        for request in self.emergency_queue.to_list():
            print(" ", request.display_info())


        print("\nStandard Queue: ")
        for request in self.standard_queue.to_list():
            print(" ", request.display_info())


        print("\nLow Queue: ")
        for request in self.low_queue.to_list():
            print(" ", request.display_info())