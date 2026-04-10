class Building:
    def __init__(self, building_id: str, name: str, location: tuple):
        self.building_id = building_id # e.g. "ICT"
        self.name = name # "Information and Comm. Tech."
        self.location = location # (lat, lon) or grid coords
        self.rooms = {}