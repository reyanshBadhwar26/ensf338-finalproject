from queue_linked_list import Queue

class RequestQueue:
    def __init__(self):
        self.queue = Queue()

    def enqueue(self, request):
        self.queue.enqueue(request)

    def dequeue(self):
        return self.queue.dequeue()

    def is_empty(self):
        return self.queue.is_empty()

if __name__ == "__main__":
    # simulating 20 requests

    request_queue = RequestQueue()

    # enqueue 20 requests
    for i in range(1, 21):
        request = f"Request #{i}"
        request_queue.enqueue(request)
        print(f"Enqueued: {request}")

    print("\n-Processing in arrival order-\n")

    # dequeue and process all
    order = 1
    while not request_queue.is_empty():
        request = request_queue.dequeue()
        print(f"Processing ({order}): {request}")
        order += 1