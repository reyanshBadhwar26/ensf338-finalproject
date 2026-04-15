"""
This module contains the BuildingLookup class, which provides efficient fast
insert, delete, and lookup operations for buildings and rooms using
Python dictionaries. It is used to support the fast building and
resource lookup feature in the campus navigation and event management system.
"""

class BuildingLookup:
    # Initializes empty dictionaries for storing buildings and rooms by ID.
    def __init__(self):
        self.buildings_by_id = {}   # building_id -> Building object
        self.rooms_by_id = {}       # room_id -> Room object

    # Inserts a building into the lookup table using its unique building ID.
    def insert_building(self, building):
        self.buildings_by_id[building.building_id] = building

    # Deletes a building from the lookup table if the ID exists.
    def delete_building(self, building_id):
        if building_id in self.buildings_by_id:
            del self.buildings_by_id[building_id]

    # Returns the building associated with the given ID, or None if not found.
    def lookup_building(self, building_id):
        return self.buildings_by_id.get(building_id)

    # Inserts a room into the lookup table using its unique room ID.
    def insert_room(self, room):
        self.rooms_by_id[room.room_id] = room

    # Deletes a room from the lookup table if the ID exists.
    def delete_room(self, room_id):
        if room_id in self.rooms_by_id:
            del self.rooms_by_id[room_id]

    # Returns the room associated with the given ID, or None if not found.
    def lookup_room(self, room_id):
        return self.rooms_by_id.get(room_id)