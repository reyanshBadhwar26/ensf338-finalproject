import os

from campus import Campus
from building_lookup import BuildingLookup
from request_queue import RequestQueue
from priority_service_queue import PriorityServiceQueue
from navigation_history import NavigationHistory
from room_event_bookings import RoomEventBookings
from map_loader import load_map_from_dot
from menu import run_main_menu


def main():
    campus = Campus()

    base_dir = os.path.dirname(__file__)
    map_path = os.path.join(base_dir, "..", "data", "campus_map.dot")

    lookup = BuildingLookup()
    request_queue = RequestQueue()
    priority_queue = PriorityServiceQueue()
    navigation_history = NavigationHistory()
    booking_system = RoomEventBookings()

    load_map_from_dot(map_path, campus)

    run_main_menu(
        campus=campus,
        lookup=lookup,
        request_queue=request_queue,
        priority_queue=priority_queue,
        navigation_history=navigation_history,
        booking_system=booking_system,
    )


if __name__ == "__main__":
    main()