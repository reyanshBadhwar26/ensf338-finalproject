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

    def add(self, start, end, path, distance):
        step = {
        "start": start,
        "end": end,
        "path": path,
        "distance": distance
        }

        self.history.push(step)

    def undo(self):
        self.history.pop()

        return self.history.peek()