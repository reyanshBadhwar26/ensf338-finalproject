# Room class.
# This file defines a room and stores its basic details and associated bookings.

class Room:
    def __init__(self, room_id: str, capacity: int, room_type: str):
        self.room_id = room_id        # Unique identifier 
        self.capacity = capacity      # Maximum number of people the room can hold
        self.room_type = room_type    # Type of room 
        self.bookings = []            # List to store bookings/events for this room