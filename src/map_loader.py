import re
from building import Building
from campus import Campus
import campus as campus

#Grid coordinates for the buildings
BUILDING_COORDS = {
    "HUNTER_COMMONS": (0, 4),
    "ARTS": (2, 5),
    "LIBRARY": (2, 3),
    "BOOKSTORE": (0, 2),

    "SCI_B": (4, 5),
    "SCI_A": (4, 3),
    "KINESIOLOGY": (6, 5),
    "GYM": (7, 3),

    "MACHALL": (2, 1),
    "ICT": (4, 1),
    "ENG_BLOCK": (6, 2),

    "ADMIN": (1, 0),
    "STUDENT_UNION": (4, 0),
    "PARKADE": (6, 0),
    "RESIDENCE": (3, -2),
}

def load_map_from_dot(filename: str, campus):
    """
    Reads a .dot file and loads buildings and pathways into the Campus object.
    """

    edge_pattern = re.compile(r'(\w+)\s*--\s*(\w+)\s*\[weight=(\d+)\];')

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            match = edge_pattern.match(line)
            if match:
                building_1 = match.group(1)
                building_2 = match.group(2)
                weight = int(match.group(3))

                # Create buildings if they do not already exist
                if building_1 not in campus.buildings:
                    campus.buildings[building_1] = Building(
                        building_id=building_1,
                        name=building_1,
                        location=BUILDING_COORDS.get(building_1, (0, 0))
                    )

                if building_2 not in campus.buildings:
                    campus.buildings[building_2] = Building(
                        building_id=building_2,
                        name=building_2,
                        location=BUILDING_COORDS.get(building_2, (0, 0))
                    )

                # Create pathway entries if missing
                if building_1 not in campus.pathways:
                    campus.pathways[building_1] = {}

                if building_2 not in campus.pathways:
                    campus.pathways[building_2] = {}

                # Undirected graph, so add both directions
                campus.pathways[building_1][building_2] = weight
                campus.pathways[building_2][building_1] = weight


# TEST USAGE 
# test = campus.Campus()
# load_map_from_dot("../data/campus_map.dot", test)
# print(test.buildings)
# print(test.pathways)