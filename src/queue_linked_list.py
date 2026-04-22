#This class implements a queue structure to be used for request and service queues

#Use a linked list to implement queue so we have efficient enqueue and dequeue
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.size = 0
        self.front = None #For tracking the first element of the queue
        self.rear = None #For tracking the last element of the queue

    def is_empty(self):
        return self.size == 0
    
    #Return the first element
    def peek(self):
        if self.is_empty():
            return None
        return self.front.data

    #Add an element to the end of the queue
    def enqueue(self, item):
        new_node = Node(item)

        #If the queue is empty both head and tail would be same node
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size = self.size + 1

    #Remove and return the first element of the queue
    def dequeue(self):
        if self.is_empty():
            raise IndexError("The queue is empty")
        
        #Remove the front node and update the front pointer to the next node
        item = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size = self.size - 1
        return item
    
    def __len__(self):
        return self.size
    
    #For printing and testing purposes, convert the queue to a list
    def to_list(self):
        items = []
        current = self.front
        while current is not None:
            items.append(current.data)
            current = current.next
        return items
    