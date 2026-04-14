from service_request import ServiceRequest
from queue_linked_list import Queue

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
        print("\nEmergency Queue:")
        emergency = self.emergency_queue.to_list()
        if not emergency:
            print("None")
        else:
            for request in emergency:
                print(" ", request.display_info())

        print("\nStandard Queue:")
        standard = self.standard_queue.to_list()
        if not standard:
            print("None")
        else:
            for request in standard:
                print(" ", request.display_info())

        print("\nLow Queue:")
        low = self.low_queue.to_list()
        if not low:
            print("None")
        else:
            for request in low:
                print(" ", request.display_info())