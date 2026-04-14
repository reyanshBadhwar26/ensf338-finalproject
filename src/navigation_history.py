class Stack:
    def __init__(self):
        self.data = []

    def push(self, value):
        self.data.append(value)

    def pop(self):
        if len(self.data) == 0:
            return None
        
        return self.data.pop()
    
    def peek(self):
        if len(self.data) == 0:
            return None
        
        return self.data[-1]
    
class NavigationHistory:
    def __init__(self):
        self.history = Stack()

    def add(self, start, end, path, time):
        step = {
        "start": start,
        "end": end,
        "path": path,
        "total_time": time
        }

        self.history.push(step)

    def undo(self):
        if self.history.peek() is None:
            return None

        if len(self.history.data) == 1:
            return self.history.peek()

        self.history.pop()
        return self.history.peek()