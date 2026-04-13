class RequestQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, request):
        self.queue.append(request)

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def is_empty(self):
        return len(self.queue) == 0


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