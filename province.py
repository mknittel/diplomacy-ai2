class Province:
    name = ""
    fleet_neighbors = [] # Reachable by fleet
    army_neighbors = [] # Reachable by army, empty for sea

    class LandProvince(Province):
        has_center = False

        def add_coast(self, loc):
            if loc not in fleet_neighbors:
                fleet_neighbors += [loc]

            if loc not in army_neighbors:
                army_neighbors += [loc]

        def add_land_neighbor(self, loc):
            if loc not in army_neighbors:
                army_neighbors += loc

        def add_sea_neighbor(self, loc):
            if loc not in fleet_neighbors:
                sea_neighbors += loc

    class SeaProvince(Province):
        def add_sea(self, loc):
            if loc not in fleet_neighbors:
                fleet_neighbors += [loc] 

    def print_data(self):
        for loc in fleet_neighbors:
            print(self.name, " is reachable by ", loc, " by fleet.")
        for loc in army_neighbors:
            print(self.name, " is reachable by ", loc, " by army.")

        if (fleet_neighbors.empty()):
            print (self.name, " has no neighbors reachable by fleet.")
        
        if (army_neighbors.empty()):
            print (self.name, " has no neighbors reachable by army.")

    def __init__(self, name):
        self.name = name
        self.is_land = True
