from campus import Campus
from building import Building
from map_loader import load_map_from_dot
from navigation import *

# Testing methods (2.1 and 2.2)
test = Campus()
load_map_from_dot("campus_map.dot", test)
print("Buildings:", test.buildings)
print("Pathways:", test.pathways)

times, previous_buildings = shortest_path(test, "ICT")
print("Distances from ICT:", times)
print("\n\nPath from ICT to RESIDENCE:", get_path(previous_buildings, "ICT", "RESIDENCE")) #Should be ICT -> Student Union -> Residence
