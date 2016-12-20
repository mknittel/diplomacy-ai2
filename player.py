class Unit:
    def __init__(self, unit_type, loc):
        self.unit_type = unit_type
        self.loc = loc

    def print_unit(self):
        print self.unit_type, "at", self.loc

class Player:
    def __init__(self, name):
        self.name = name
        self.centers = []
        self.home_centers = []
        self.units = {}
        self.retreats = {}

    def num_centers(self):
        return len(self.centers)

    def num_home_centers(self):
        return len(self.home_centers)

    def num_units(self):
        return len(self.units)

    def lose_center(self, loc):
        self.centers.remove(loc)

    def gain_center(self, loc):
        if loc not in self.centers:
            self.centers.append(loc)

    def build(self, unit_type, loc):
        unit = Unit(unit_type, loc)
        self.units[loc] = unit

    def disband(self, loc):
        self.units.pop(loc, None)

    def move(self, start, dest):
        unit = self.units.pop(start, None)

        if unit == None:
            unit = self.retreats.pop(start, None)

        if unit != None:
            unit.loc = dest
            self.units[dest] = unit

    def place_retreat(self, start, dest):
        unit = self.retreats.pop(start, None)
        unit.loc = dest
        self.units[dest] = unit

    def disband_retreat(self, loc):
        self.retreats.pop(loc, None)

    # Assumes valid loc
    def get_unit_type(self, loc):
        unit = self.units[loc]
        return unit.unit_type

    def clean_retreats(self):
        self.retreats.clear()

    def retreat(self, loc):
        unit = self.units.pop(loc, None)
        self.retreats[loc] = unit

    def print_data(self):
        print self.name, "has",  self.num_centers(), "centers:", self.centers, "and units:"

        for unit in self.units.values():
            unit.print_unit()

        print "And retreat units:"

        for unit in self.retreats.values():
            unit.print_unit()
