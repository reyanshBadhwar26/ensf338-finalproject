class BuildingLookup:
    def __init__(self):
        self.buildings_by_id = {}   
        self.rooms_by_id = {}       

    def insert_building(self, building):
        self.buildings_by_id[building.building_id] = building

    def delete_building(self, building_id):
        if building_id in self.buildings_by_id:
            del self.buildings_by_id[building_id]

    def lookup_building(self, building_id):
        return self.buildings_by_id.get(building_id)

    def insert_room(self, room):
        self.rooms_by_id[room.room_id] = room

    def delete_room(self, room_id):
        if room_id in self.rooms_by_id:
            del self.rooms_by_id[room_id]

    def lookup_room(self, room_id):
        return self.rooms_by_id.get(room_id)