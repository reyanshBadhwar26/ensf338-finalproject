# Simple list based stack implementation for undo feature of navigation 
class Stack:
    def __init__(self):
        self.data = []

    # Add an element to the top of the stack
    def push(self, value):
        self.data.append(value)

    # Remove and return the last element of the stack
    def pop(self):
        if len(self.data) == 0:
            return None
        
        return self.data.pop()
    
    # Return the last element without removing it
    def peek(self):
        if len(self.data) == 0:
            return None
        
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0
    

# Tracks navigation history using a stack
class NavigationHistory:
    def __init__(self):
        self.history = Stack()

    # Add a new route to history
    # To record the session, we can store the start and end locations, the path taken, and the total time for the route
    def add(self, start, end, path, time):
        step = {
        "start": start,
        "end": end,
        "path": path,
        "total_time": time
        }

        self.history.push(step)

    # Undo last action and return previous
    def undo(self):
        if self.history.is_empty():
            return None
        
        self.history.pop()
        return self.history.peek()
    
# Demo to show undo works (at least 10 times)
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