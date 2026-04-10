class Campus:
    def __init__(self):
        self.buildings = {} # building_id -> Building
        self.pathways = {}  # Hashmap of building_id -> {other_building_id: distance} for quick lookup of distances between buildings


# self.pathways = {
#     "ICT": {"ENG_BLOCK": 6, "LIBRARY": 4},
#     "ENG_BLOCK": {"ICT": 6, "SCI_A": 2}
# }