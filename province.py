class Province:
    def print_data(self):
        for loc in self.fleet_neighbors:
            print self.name, "can reach", loc, "by fleet."
        for loc in self.army_neighbors:
            print self.name, "can reach", loc, "by army."

        if not self.fleet_neighbors:
            print self.name, "has no neighbors it can reach by fleet."
        
        if not self.army_neighbors:
            print self.name, "has no neighbors it can reach by army."

    def __init__(self, name):
        self.name = name
        self.is_land = True
        self.fleet_neighbors = [] # Reachable by fleet
        self.army_neighbors = [] # Reachable by army, empty for sea

class SeaProvince(Province):
    def add_sea_neighbor(self, loc):
        if loc not in self.fleet_neighbors:
            self.fleet_neighbors += [loc] 

    def add_land_neighbor(self, loc):
        if loc not in self.fleet_neighbors:
            self.fleet_neighbors += [loc]

        if loc not in self.army_neighbors:
            self.army_neighbors += [loc]

    def __init__(self, name):
        Province.__init__(self, name)
    
    def print_data(self):
        Province.print_data(self)
        self.is_land = False

class LandProvince(Province):
    def add_coast(self, loc):
        if loc not in self.fleet_neighbors:
            self.fleet_neighbors += [loc]

        if loc not in self.army_neighbors:
            self.army_neighbors += [loc]

    def add_land_neighbor(self, loc):
        if loc not in self.army_neighbors:
            self.army_neighbors += [loc]

    def add_sea_neighbor(self, loc):
        if loc not in self.fleet_neighbors:
            self.fleet_neighbors += [loc]

    def __init__(self, name):
        self.has_center = False
        Province.__init__(self, name)

    def print_data(self):
        Province.print_data(self)
