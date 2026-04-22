# Menu and user interface.
# This file handles user input and provides access to navigation, booking, lookup, and request features.

from datetime import datetime, time, timedelta

from building import Building
from room import Room
from navigation import get_shortest_path
from room_event_bookings import Booking
from service_request import ServiceRequest
import random


# Prints a blank line to visually separate menu screens.
def clear_screen():
    print("\n")


# Repeatedly prompts until the user enters a non-empty string.
def prompt_nonempty(message: str) -> str:
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Input cannot be empty.")


# Repeatedly prompts until the user enters a valid integer.
def prompt_int(message: str) -> int:
    while True:
        value = input(message).strip()
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid integer.")


# Repeatedly prompts until the user enters a valid date in YYYY-MM-DD format.
def prompt_date(message: str):
    while True:
        value = input(message).strip()
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            print("Use format YYYY-MM-DD")


# Repeatedly prompts until the user enters a valid time in HH:MM format.
def prompt_time(message: str):
    while True:
        value = input(message).strip()
        try:
            return datetime.strptime(value, "%H:%M").time()
        except ValueError:
            print("Use format HH:MM")


# Displays all valid building IDs currently stored in the campus map.
def print_valid_building_ids(campus):
    print("Valid building IDs:")
    print(", ".join(sorted(campus.buildings.keys())))


# Repeatedly prompts until the user enters a valid building ID.
# Also normalizes the input by converting to uppercase and replacing spaces with underscores.
def prompt_valid_building_id(campus, message: str) -> str:
    while True:
        building_id = "_".join(input(message).strip().upper().split())
        if building_id in campus.buildings:
            return building_id

        print("Invalid building ID.")
        print_valid_building_ids(campus)


# Displays all valid room IDs for a specific building.
def print_valid_room_ids(campus, building_id: str):
    room_ids = sorted(campus.buildings[building_id].rooms.keys())
    print(f"\nValid room IDs for {building_id}:")
    print(", ".join(room_ids))


# Repeatedly prompts until the user enters a valid room ID for the chosen building.
def prompt_valid_room_id(campus, building_id: str, message: str = "Room ID: ") -> str:
    while True:
        room_id = input(message).strip().upper()
        if room_id in campus.buildings[building_id].rooms:
            return room_id

        print("Invalid room ID.")
        print_valid_room_ids(campus, building_id)


# Ensures that each building has at least two sample rooms available.
# This helps support booking and lookup demos even if no rooms were preloaded.
def ensure_sample_rooms(campus):
    for building_id, building in campus.buildings.items():
        if not hasattr(building, "rooms") or building.rooms is None:
            building.rooms = {}

        if len(building.rooms) == 0:
            room1_id = f"{building_id}-101"
            room2_id = f"{building_id}-201"
            building.rooms[room1_id] = Room(room1_id, 40, "lecture")
            building.rooms[room2_id] = Room(room2_id, 25, "lab")


# Clears and reloads the hash-table lookup structure using the current campus data.
def seed_lookup_from_campus(campus, lookup):
    lookup.buildings_by_id.clear()
    lookup.rooms_by_id.clear()

    for building in campus.buildings.values():
        lookup.insert_building(building)
        for room in building.rooms.values():
            lookup.insert_room(room)


# Adds demo bookings to the booking system for testing and demonstrations.
def seed_demo_bookings(booking_system):
    demo = [
        Booking(
            "ICT-101",
            datetime(2026, 4, 20).date(),
            datetime.strptime("09:00", "%H:%M").time(),
            datetime.strptime("10:00", "%H:%M").time(),
            "Math Lecture",
        ),
        Booking(
            "ICT-101",
            datetime(2026, 4, 20).date(),
            datetime.strptime("10:30", "%H:%M").time(),
            datetime.strptime("12:00", "%H:%M").time(),
            "Club Meeting",
        ),
        Booking(
            "ENG_BLOCK-201",
            datetime(2026, 4, 20).date(),
            datetime.strptime("13:00", "%H:%M").time(),
            datetime.strptime("14:00", "%H:%M").time(),
            "Lab Session",
        ),
        Booking(
            "SCI_A-201",
            datetime(2026, 4, 20).date(),
            datetime.strptime("15:00", "%H:%M").time(),
            datetime.strptime("17:00", "%H:%M").time(),
            "Hackathon Prep",
        ),
    ]

    # Tracks how many bookings were successfully inserted.
    count = 0
    for booking in demo:
        if booking_system.add_booking(booking):
            count += 1

    # Additional generated bookings for a larger demo dataset.
    rooms = ["ICT-101", "ENG_BLOCK-201", "SCI_A-201", "ICT-102", "LAB-1"]
    event_names = ["Study Session", "Project Meeting", "Team Sync", "Workshop", "Lab Session", "Office Hours", "Group Discussion", "Seminar", "Review Session", "Hackathon"]
    base_date = datetime(2026, 4, 21).date()

    # Generates bookings across 20 days for multiple rooms.
    for day_offset in range(20):  # 20 days
        for i, room in enumerate(rooms):
            start_hour = 8 + (i * 2)
            booking = Booking(
                room,
                base_date + timedelta(days=day_offset),
                time(start_hour, 0),
                time(start_hour + 1, 0),
                random.choice(event_names)
            )
            if booking_system.add_booking(booking):
                count += 1
        
    return count


# Displays the main menu options.
def print_main_menu():
    print("Campus Navigation and Event Management System")
    print("-" * 46)
    print("1. Shortest path navigation")
    print("2. Undo last navigation")
    print("3. Show navigation history")
    print("4. Room and event booking system")
    print("5. Priority service queue")
    print("6. Fast building / room lookup")
    print("7. Incoming request pipeline")
    print("8. Demo setup")
    print("0. Exit")


# Runs the main menu loop and dispatches user choices to the correct feature.
def run_main_menu(campus, lookup, request_queue, priority_queue, navigation_history, booking_system):
    ensure_sample_rooms(campus)
    seed_lookup_from_campus(campus, lookup)

    while True:
        clear_screen()
        print_main_menu()
        choice = input("\n>> ").strip()

        if choice == "1":
            handle_shortest_path(campus, navigation_history)
        elif choice == "2":
            handle_undo_navigation(navigation_history)
        elif choice == "3":
            handle_show_navigation_history(navigation_history)
        elif choice == "4":
            booking_menu(campus, booking_system)
        elif choice == "5":
            priority_queue_menu(priority_queue)
        elif choice == "6":
            lookup_menu(campus, lookup)
        elif choice == "7":
            request_pipeline_menu(campus, request_queue)
        elif choice == "8":
            run_demo_setup(campus, lookup, booking_system)
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please pick a number from 0 to 8.")


# Handles shortest path queries and stores successful routes in navigation history.
def handle_shortest_path(campus, navigation_history):
    clear_screen()
    print("Shortest Path Navigation")
    print("-" * 28)

    if not campus.buildings:
        print("No campus map loaded.")
        return

    print_valid_building_ids(campus)
    start = prompt_valid_building_id(campus, "Enter source building ID: ")
    end = prompt_valid_building_id(campus, "Enter destination building ID: ")

    result = get_shortest_path(campus, start, end)

    if result is not None:
        navigation_history.add(result["start"], result["end"], result["path"], result["total_time"])
        print("\nRoute saved to history.")


# Undoes the most recent navigation action and restores the previous route if available.
def handle_undo_navigation(navigation_history):
    clear_screen()
    print("Undo Navigation")
    print("-" * 16)

    previous = navigation_history.undo()

    if previous is None:
        print("No earlier navigation history available.")
    else:
        print("Reverted to previous navigation:")
        print(f"Start: {previous['start']}")
        print(f"End: {previous['end']}")
        print(f"Time: {previous['total_time']} minutes")
        if isinstance(previous["path"], list):
            print("Path:", " -> ".join(previous["path"]))
        else:
            print("Path:", previous["path"])


# Displays all saved navigation history entries.
def handle_show_navigation_history(navigation_history):
    clear_screen()
    print("Navigation History")
    print("-" * 18)

    items = navigation_history.history.data

    if not items:
        print("No saved routes.")
    else:
        for i, item in enumerate(items, start=1):
            path = item["path"]
            path = " -> ".join(path) if isinstance(path, list) else path
            print(
                f"{i}. {item['start']} -> {item['end']} | "
                f"Time: {item['total_time']} minutes | Path: {path}"
            )


# Submenu for all booking-related features.
def booking_menu(campus, booking_system):
    while True:
        clear_screen()
        print("Room and Event Booking System")
        print("-" * 29)
        print("1. Add booking")
        print("2. Remove booking")
        print("3. Get exact booking")
        print("4. Show events on a day")
        print("5. Query events in a time range")
        print("6. Show next upcoming event")
        print("7. Print booking AVL tree - Bonus 2.7")
        print("0. Back")

        choice = input("\n>> ").strip()

        if choice == "1":
            add_booking(campus, booking_system)
        elif choice == "2":
            remove_booking(campus, booking_system)
        elif choice == "3":
            get_exact_booking(campus, booking_system)
        elif choice == "4":
            show_events_on_day(booking_system)
        elif choice == "5":
            query_time_range(booking_system)
        elif choice == "6":
            show_next_upcoming(booking_system)
        elif choice == "7":
            show_booking_avl_tree(booking_system)
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please pick a number from 0 to 7.")


# Adds a new booking after validating building, room, date, and times.
def add_booking(campus, booking_system):
    clear_screen()
    print("Add Booking")
    print("-" * 11)

    building_id = prompt_valid_building_id(campus, "Building ID: ")
    print_valid_room_ids(campus, building_id)
    room_id = prompt_valid_room_id(campus, building_id)

    event_name = prompt_nonempty("Event name: ")
    event_date = prompt_date("Date (YYYY-MM-DD): ")
    start_time = prompt_time("Start time (HH:MM): ")
    end_time = prompt_time("End time   (HH:MM): ")

    # Prevents invalid time ranges.
    if end_time <= start_time:
        print("End time must be after start time.")
        return

    booking = Booking(room_id, event_date, start_time, end_time, event_name)
    success = booking_system.add_booking(booking)

    if success:
        print("Booking added successfully.")
    else:
        print("Could not add booking. It may already exist or overlap.")


# Removes a booking using room, date, and start time as the lookup key.
def remove_booking(campus, booking_system):
    clear_screen()
    print("Remove Booking")
    print("-" * 14)

    building_id = prompt_valid_building_id(campus, "Building ID: ")
    print_valid_room_ids(campus, building_id)
    room_id = prompt_valid_room_id(campus, building_id)
    event_date = prompt_date("Date (YYYY-MM-DD): ")
    start_time = prompt_time("Start time (HH:MM): ")

    removed = booking_system.remove_booking(room_id, event_date, start_time)

    if removed:
        print("Booking removed.")
    else:
        print("Booking not found.")


# Retrieves and displays one exact booking if it exists.
def get_exact_booking(campus, booking_system):
    clear_screen()
    print("Get Exact Booking")
    print("-" * 17)

    building_id = prompt_valid_building_id(campus, "Building ID: ")
    print_valid_room_ids(campus, building_id)
    room_id = prompt_valid_room_id(campus, building_id)
    event_date = prompt_date("Date (YYYY-MM-DD): ")
    start_time = prompt_time("Start time (HH:MM): ")

    booking = booking_system.get_booking(room_id, event_date, start_time)

    if booking is None:
        print("No booking found.")
    else:
        print(booking)


# Displays all events scheduled on a specific date.
def show_events_on_day(booking_system):
    clear_screen()
    print("Events on a Day")
    print("-" * 15)

    event_date = prompt_date("Date (YYYY-MM-DD): ")
    events = booking_system.get_events_on_day(event_date)

    if not events:
        print("No events found for that day.")
    else:
        for event in events:
            print(event)


# Displays all events within a given time range on a specific date.
def query_time_range(booking_system):
    clear_screen()
    print("Query Events in Time Range")
    print("-" * 26)

    event_date = prompt_date("Date (YYYY-MM-DD): ")
    start_time = prompt_time("Start time (HH:MM): ")
    end_time = prompt_time("End time   (HH:MM): ")

    # Prevents invalid time ranges.
    if end_time <= start_time:
        print("End time must be after start time.")
        return

    events = booking_system.get_events_in_time_range(event_date, start_time, end_time)

    if not events:
        print("No events found in that time range.")
    else:
        for event in events:
            print(event)


# Shows the next event scheduled after the current system time.
def show_next_upcoming(booking_system):
    clear_screen()
    print("Next Upcoming Event")
    print("-" * 20)

    next_event = booking_system.get_next_upcoming_event(datetime.now())

    if next_event is None:
        print("No upcoming events.")
    else:
        print(next_event)


# Submenu for priority-based service requests.
def priority_queue_menu(priority_queue):
    while True:
        clear_screen()
        print("Priority Service Queue")
        print("-" * 22)
        print("1. Add service request")
        print("2. Serve next request")
        print("3. Peek next request")
        print("4. Display all queues")
        print("0. Back")

        choice = input("\n>> ").strip()

        if choice == "1":
            add_service_request(priority_queue)
        elif choice == "2":
            serve_next_request(priority_queue)
        elif choice == "3":
            peek_next_request(priority_queue)
        elif choice == "4":
            display_priority_queues(priority_queue)
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please pick a number from 0 to 4.")


# Adds a service request with one of three allowed priority levels.
def add_service_request(priority_queue):
    clear_screen()
    print("Add Service Request")
    print("-" * 19)

    request_id = prompt_nonempty("Request ID: ")
    service_type = prompt_nonempty("Service type: ")
    description = prompt_nonempty("Description: ")
    requester_name = prompt_nonempty("Requester name: ")

    # Ensures the priority entered is valid.
    while True:
        priority = input("Priority (Emergency / Standard / Low): ").strip().title()
        if priority in {"Emergency", "Standard", "Low"}:
            break
        print("Invalid priority.")

    request = ServiceRequest(
        request_id,
        service_type,
        description,
        priority,
        requester_name
    )

    priority_queue.add_request(request)
    print("Service request added.")


# Removes and displays the highest-priority pending request.
def serve_next_request(priority_queue):
    clear_screen()
    print("Serve Next Request")
    print("-" * 18)

    request = priority_queue.serve_next_request()

    if request is None:
        print("No pending requests.")
    else:
        print("Serving:")
        print(request.display_info())


# Displays the next request that would be served without removing it.
def peek_next_request(priority_queue):
    clear_screen()
    print("Peek Next Request")
    print("-" * 17)

    request = priority_queue.peek_next_request()

    if request is None:
        print("No pending requests.")
    else:
        print(request.display_info())


# Displays all service requests across all priority levels.
def display_priority_queues(priority_queue):
    clear_screen()
    print("All Priority Queues")
    print("-" * 19)
    priority_queue.display_queue()


# Submenu for the fast building and room lookup feature.
def lookup_menu(campus, lookup):
    while True:
        clear_screen()
        print("Fast Building / Room Lookup")
        print("-" * 28)
        print("1. Insert building")
        print("2. Delete building")
        print("3. Lookup building")
        print("4. Insert room")
        print("5. Delete room")
        print("6. Lookup room")
        print("7. Show all buildings")
        print("0. Back")

        choice = input("\n>> ").strip()

        if choice == "1":
            insert_building(campus, lookup)
        elif choice == "2":
            delete_building(campus, lookup)
        elif choice == "3":
            lookup_building(campus, lookup)
        elif choice == "4":
            insert_room(campus, lookup)
        elif choice == "5":
            delete_room(campus, lookup)
        elif choice == "6":
            lookup_room(lookup)
        elif choice == "7":
            show_all_buildings(campus)
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please pick a number from 0 to 7.")


# Inserts a new building into both the campus map and the lookup table.
def insert_building(campus, lookup):
    clear_screen()
    print("Insert Building")
    print("-" * 15)

    building_id = prompt_nonempty("Building ID: ").upper()
    if building_id in campus.buildings:
        print("That building already exists.")
        return

    name = prompt_nonempty("Building name: ")
    x = prompt_int("Location x-coordinate: ")
    y = prompt_int("Location y-coordinate: ")

    building = Building(building_id, name, (x, y))
    building.rooms = {}

    campus.buildings[building_id] = building

    # Ensures the building also exists in the pathway graph.
    if building_id not in campus.pathways:
        campus.pathways[building_id] = {}

    lookup.insert_building(building)
    print("Building inserted.")


# Deletes a building and removes all related rooms and pathway connections.
def delete_building(campus, lookup):
    clear_screen()
    print("Delete Building")
    print("-" * 15)

    building_id = prompt_valid_building_id(campus, "Building ID: ")
    building = campus.buildings[building_id]

    # Remove the building's rooms from the lookup table first.
    for room_id in list(building.rooms.keys()):
        lookup.delete_room(room_id)

    del campus.buildings[building_id]
    lookup.delete_building(building_id)

    # Remove the building from the campus graph.
    if building_id in campus.pathways:
        del campus.pathways[building_id]

    # Remove all edges pointing to that building.
    for other in campus.pathways:
        if building_id in campus.pathways[other]:
            del campus.pathways[other][building_id]

    print("Building deleted.")


# Looks up and displays one building and all of its rooms.
def lookup_building(campus, lookup):
    clear_screen()
    print("Lookup Building")
    print("-" * 15)

    building_id = prompt_valid_building_id(campus, "Building ID: ")
    building = lookup.lookup_building(building_id)

    if building is None:
        print("Building not found.")
    else:
        print(f"ID: {building.building_id}")
        print(f"Name: {building.name}")
        print(f"Location: {building.location}")
        print("Rooms:")
        if building.rooms:
            for room in building.rooms.values():
                print(f"  {room.room_id} | capacity={room.capacity} | type={room.room_type}")
        else:
            print("  none")


# Inserts a new room into a selected building and the lookup table.
def insert_room(campus, lookup):
    clear_screen()
    print("Insert Room")
    print("-" * 11)

    building_id = prompt_valid_building_id(campus, "Building ID: ")
    room_id = prompt_nonempty("Room ID: ").upper()
    capacity = prompt_int("Capacity: ")
    room_type = prompt_nonempty("Room type: ")

    if room_id in campus.buildings[building_id].rooms:
        print("Room already exists in that building.")
        return

    room = Room(room_id, capacity, room_type)
    campus.buildings[building_id].rooms[room_id] = room
    lookup.insert_room(room)

    print("Room inserted.")


# Deletes a room from both the building and the lookup table.
def delete_room(campus, lookup):
    clear_screen()
    print("Delete Room")
    print("-" * 12)

    building_id = prompt_valid_building_id(campus, "Building ID: ")
    print_valid_room_ids(campus, building_id)
    room_id = prompt_valid_room_id(campus, building_id)

    del campus.buildings[building_id].rooms[room_id]
    lookup.delete_room(room_id)

    print("Room deleted.")


# Looks up a room by exact room ID, or suggests partial matches if no exact match is found.
def lookup_room(lookup):
    clear_screen()
    print("Lookup Room")
    print("-" * 11)

    while True:
        user_input = input("Room ID (press Enter to cancel): ").strip()

        if user_input == "":
            print("Room lookup cancelled.")
            return

        # Keep original input for display, normalize a copy for searching
        search_text = "_".join(user_input.upper().split())

        room = lookup.lookup_room(search_text)

        if room is not None:
            print(f"Room ID: {room.room_id}")
            print(f"Capacity: {room.capacity}")
            print(f"Type: {room.room_type}")
            return

        # Stores partial matches if exact lookup fails.
        matches = []
        for stored_room in lookup.rooms_by_id.values():
            if search_text in stored_room.room_id.upper():
                matches.append(stored_room)

        print(f'No exact room found for "{user_input}".')

        if matches:
            print("Rooms found containing that text:")
            for match in matches:
                print(f"  {match.room_id} | capacity={match.capacity} | type={match.room_type}")
            print("Please enter the full correct room ID.\n")
        else:
            print(f'No rooms found containing "{user_input}".')
            print("Please try again.\n")


# Displays all buildings currently loaded in the campus system.
def show_all_buildings(campus):
    clear_screen()
    print("All Buildings")
    print("-" * 13)

    if not campus.buildings:
        print("No buildings loaded.")
    else:
        for i, building_id in enumerate(sorted(campus.buildings.keys()), start=1):
            print(f"{i}. {building_id}")


# Submenu for incoming request pipeline operations.
def request_pipeline_menu(campus, request_queue):
    while True:
        clear_screen()
        print("Incoming Request Pipeline")
        print("-" * 25)
        print("1. Enqueue navigation request")
        print("2. Enqueue service request")
        print("3. Process next request")
        print("4. Show pending requests")
        print("5. Simulate 20 sequential requests")
        print("0. Back")

        choice = input("\n>> ").strip()

        if choice == "1":
            enqueue_navigation_request(campus, request_queue)
        elif choice == "2":
            enqueue_service_pipeline_request(request_queue)
        elif choice == "3":
            process_next_request(request_queue)
        elif choice == "4":
            show_pending_requests(request_queue)
        elif choice == "5":
            simulate_20_requests(request_queue)
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please pick a number from 0 to 5.")


# Enqueues a navigation request in FIFO order.
def enqueue_navigation_request(campus, request_queue):
    clear_screen()
    print("Enqueue Navigation Request")
    print("-" * 26)

    print_valid_building_ids(campus)
    source = prompt_valid_building_id(campus, "Source building: ")
    destination = prompt_valid_building_id(campus, "Destination building: ")

    request = {
        "type": "navigation",
        "source": source,
        "destination": destination,
    }

    request_queue.enqueue(request)
    print("Navigation request enqueued.")


# Enqueues a generic service request in FIFO order.
def enqueue_service_pipeline_request(request_queue):
    clear_screen()
    print("Enqueue Service Request")
    print("-" * 23)

    request_id = prompt_nonempty("Request ID: ")
    description = prompt_nonempty("Description: ")

    request = {
        "type": "service",
        "request_id": request_id,
        "description": description,
    }

    request_queue.enqueue(request)
    print("Service request enqueued.")


# Processes the next request in arrival order.
def process_next_request(request_queue):
    clear_screen()
    print("Process Next Request")
    print("-" * 20)

    if request_queue.is_empty():
        print("No pending requests.")
        return

    request = request_queue.dequeue()
    print("Processed request:")
    print(request)


# Displays all currently pending requests in the queue.
def show_pending_requests(request_queue):
    clear_screen()
    print("Pending Requests")
    print("-" * 16)

    if request_queue.is_empty():
        print("No pending requests.")
    else:
        pending = request_queue.queue.to_list()
        for i, request in enumerate(pending, start=1):
            print(f"{i}. {request}")


# Demonstrates FIFO processing using 20 automatically generated requests.
def simulate_20_requests(request_queue):
    clear_screen()
    print("Simulate 20 Sequential Requests")
    print("-" * 31)

    generated_requests = []

    # Creates 20 alternating service and navigation requests.
    for i in range(1, 21):
        if i % 2 == 0:
            request = {
                "type": "navigation",
                "source": "ICT",
                "destination": "RESIDENCE",
                "number": i,
            }
        else:
            request = {
                "type": "service",
                "request_id": f"REQ-{i}",
                "description": f"Generated request {i}",
                "number": i,
            }

        generated_requests.append(request)
        request_queue.enqueue(request)

    print("Step 1: Requests enqueued in arrival order\n")
    for i, request in enumerate(generated_requests, start=1):
        print(f"Enqueue {i}: {request}")

    print("\nStep 2: Requests processed in the same FIFO order\n")
    count = 1
    while not request_queue.is_empty():
        request = request_queue.dequeue()
        print(f"Dequeue {count}: {request}")
        count += 1


# Runs a quick setup for demos by ensuring rooms, refreshing lookup, and adding sample bookings.
def run_demo_setup(campus, lookup, booking_system):
    clear_screen()
    print("Demo Setup")
    print("-" * 10)

    ensure_sample_rooms(campus)
    seed_lookup_from_campus(campus, lookup)
    added = seed_demo_bookings(booking_system)

    print("Sample rooms ensured.")
    print("Lookup refreshed.")
    print(f"Sample bookings added: {added}")


# Bonus feature: prints the AVL tree used as the balanced event index.
def show_booking_avl_tree(booking_system):
    clear_screen()
    print("Booking AVL Tree")
    print("-" * 16)

    if not hasattr(booking_system, "avl_index"):
        print("AVL index is not set up in the booking system.")
        return

    if booking_system.avl_index.root is None:
        print("The booking AVL tree is empty.")
        return

    print("This tree is the bonus balanced event index.\n")
    booking_system.avl_index.print_tree()

    # If available, also checks whether the AVL tree remains balanced.
    if hasattr(booking_system.avl_index, "is_balanced"):
        print("\nAVL balance valid:", booking_system.avl_index.is_balanced())