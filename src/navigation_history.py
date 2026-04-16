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

    def is_empty(self):
        return len(self.data) == 0
    
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
        if self.history.is_empty():
            return None
        
        self.history.pop()
        return self.history.peek()
    
#Demonstration to show that it works with atleast 10 undos
def demo_undo():
    history = NavigationHistory()

    # Add 11 routes
    for i in range(11):
        history.add(f"A{i}", f"B{i}", [f"A{i}", f"B{i}"], i)

    print("Initial history size:", len(history.history.data))

    # Undo 10 times
    for i in range(10):
        prev = history.undo()
        print(f"Undo {i+1}: ", prev)

if __name__ == "__main__":
    demo_undo()