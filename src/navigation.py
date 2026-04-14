# Min-heap to be used for Dijkstra's algorithm to find the shortest path in the graph
class Heap:
    def __init__(self):
        self.data = []

    # Turns a list into a min-heap
    def heapify(self, values):
        self.data = values.copy()

        # Start from the last parent and move upward
        for i in range(len(self.data) // 2 - 1, -1, -1):
            self.bubble_down(i)

        return self.data

    def enqueue(self, value):
        self.data.append(value)
        self.bubble_up(len(self.data) - 1)

    def dequeue(self):
        if len(self.data) == 0:
            return None

        if len(self.data) == 1:
            return self.data.pop()

        root = self.data[0]
        self.data[0] = self.data.pop()
        self.bubble_down(0)
        return root

    def is_empty(self):
        return len(self.data) == 0

    def bubble_up(self, index):
        while index > 0:
            parent = (index - 1) // 2

            if self.data[index] < self.data[parent]:
                self.data[index], self.data[parent] = self.data[parent], self.data[index]
                index = parent
            else:
                break

    def bubble_down(self, index):
        size = len(self.data)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < size and self.data[left] < self.data[smallest]:
                smallest = left

            if right < size and self.data[right] < self.data[smallest]:
                smallest = right

            if smallest != index:
                self.data[index], self.data[smallest] = self.data[smallest], self.data[index]
                index = smallest
            else:
                break

# Dijkstra's algorithm to find shortest path 
def shortest_path(campus_graph, start_building):
    
    if start_building not in campus_graph.pathways:
        return None

    times = {}
    previous_buildings = {}
    
    for building in campus_graph.pathways:
        times[building] = float('inf')
        previous_buildings[building] = None

    times[start_building] = 0

    heap = Heap()
    heap.enqueue((0, start_building)) # use a tuple to compare using distance

    visited = set()

    while heap.is_empty() == False:
        current_dist, current_vertex = heap.dequeue()

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        for neighbor, weight in campus_graph.pathways[current_vertex].items():
            if neighbor in visited:
                continue

            new_dist = current_dist + weight

            if new_dist < times[neighbor]:
                times[neighbor] = new_dist
                previous_buildings[neighbor] = current_vertex
                heap.enqueue((new_dist, neighbor))

    return times, previous_buildings

def get_path(previous_buildings, start_building, end_building):
    path = []
    current = end_building

    while current is not None:
        path.append(current)
        current = previous_buildings[current]

    path.reverse()

    if path and path[0] == start_building:
        return path
    else:
        return None

def get_shortest_path(campus_graph, start_building, end_building):

    if start_building not in campus_graph.pathways:
        print(f"Invalid start building: {start_building}")
        return None

    if end_building not in campus_graph.pathways:
        print(f"Invalid destination building: {end_building}")
        return None

    result = shortest_path(campus_graph, start_building)
    if result is None:
        print("Path can not be computed")
        return None

    times, previous_buildings = result
    path = get_path(previous_buildings, start_building, end_building)

    if path is None:
        print(f"No route found from {start_building} to {end_building}.")
        return None

    total_distance = times[end_building]

    # Display the route
    print(f"\nShortest route from {start_building} to {end_building}:")
    print(" -> ".join(path))
    print(f"Total travel time: {total_distance}")

    # Return for history tracking
    return {
        "start": start_building,
        "end": end_building,
        "path": path,
        "total_time": total_distance
    }
