from queue_linked_list import Queue

class RequestQueue:
    """A request queue that uses a linked list-based Queue to manage incoming requests in FIFO order."""
    def __init__(self):
        # Initialize the Queue
        self.queue = Queue()

    def enqueue(self, request):
        # Add a new request to the end of the queue
        self.queue.enqueue(request)

    def dequeue(self):
        # Remove and return the queue the request at the front of the queue
        return self.queue.dequeue()

    def is_empty(self):
        # Returns True if there are no pending requests in the queue
        return self.queue.is_empty()

if __name__ == "__main__":
    # We simulate enqueueing and processing 20 requests in arrival order (FIFO)

    request_queue = RequestQueue()

    # Here we enqueue 20 requests and number them 1-20
    for i in range(1, 21):
        request = f"Request #{i}"
        request_queue.enqueue(request)
        print(f"Enqueued: {request}")

    print("\n-Processing in arrival order-\n")

    # Here we dequeue and process all requests in the exact order they were recieved
    order = 1 # Will be used to number the order
    while not request_queue.is_empty(): # Making sure we have requests
        request = request_queue.dequeue() # Removing a request
        print(f"Processing ({order}): {request}") 
        order += 1 