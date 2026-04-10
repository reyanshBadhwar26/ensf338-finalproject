class Room:
    def __init__ (self, room_id: str, capacity: int, room_type: str):
        self.room_id = room_id
        self.capacity = capacity
        self.room_type = room_type
        self.bookings = []
    
    