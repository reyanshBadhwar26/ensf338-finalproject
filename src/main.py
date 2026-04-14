from campus import Campus
from building import Building
from map_loader import load_map_from_dot
from navigation import *
from navigation_history import NavigationHistory

# Testing methods (2.1 and 2.2)
test = Campus()
load_map_from_dot("../data/campus_map.dot", test)

route = get_shortest_path(test, "BOOKSTORE", "KINESIOLOGY")

# After getting the route, we can add it to the navigation history
history = NavigationHistory()
if route is not None:
    history.add(route["start"], route["end"], route["path"], route["total_time"])

