from priority_service_queue import PriorityServiceQueue

class Campus:
    def __init__(self):
        self.buildings = {} # building_id -> Building
        self.pathways = {}  # Hashmap of building_id -> {other_building_id: distance} for quick lookup of distances between buildings
        self.service_queue = PriorityServiceQueue()

    def add_service_request(self, request):
        self.service_queue.add_request(request)
    
    def serve_next_service_request(self):
        return self.service_queue.serve_next_request()




# self.pathways = {
#     "ICT": {"ENG_BLOCK": 6, "LIBRARY": 4},
#     "ENG_BLOCK": {"ICT": 6, "SCI_A": 2}
# }