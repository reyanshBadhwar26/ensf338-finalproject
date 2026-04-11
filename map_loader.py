import re
from building import Building
from campus import Campus
import campus


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
                        location=(0, 0)
                    )

                if building_2 not in campus.buildings:
                    campus.buildings[building_2] = Building(
                        building_id=building_2,
                        name=building_2,
                        location=(0, 0)
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
test = campus.Campus()
load_map_from_dot("campus_map.dot", test)
print(test.buildings)
print(test.pathways)