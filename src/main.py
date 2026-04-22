# Main entry point for the Campus Navigation and Event Management System.
# This file initializes the core components, loads the campus map, and starts the main menu.

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
    # Create the main campus object that stores buildings and pathways.
    campus = Campus()

    # Build the file path to the campus map data file.
    base_dir = os.path.dirname(__file__)
    map_path = os.path.join(base_dir, "..", "data", "campus_map.dot")

    # Initialize all major system components.
    lookup = BuildingLookup()                  # Fast building/room lookup system
    request_queue = RequestQueue()             # FIFO queue for incoming requests
    priority_queue = PriorityServiceQueue()    # Priority queue for urgent service requests
    navigation_history = NavigationHistory()   # Stores previous navigation routes for undo
    booking_system = RoomEventBookings()       # Manages room bookings and event schedules

    # Load the campus graph from the DOT file into the campus object.
    load_map_from_dot(map_path, campus)

    # Start the interactive main menu and pass in all system components.
    run_main_menu(
        campus=campus,
        lookup=lookup,
        request_queue=request_queue,
        priority_queue=priority_queue,
        navigation_history=navigation_history,
        booking_system=booking_system,
    )


# Run the program only when this file is executed directly.
if __name__ == "__main__":
    main()