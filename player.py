class Player:
    def __init__(self, name):
        self.name = name
        self.centers = []
        self.units = []

    def num_centers(self):
        return len(self.centers)

    def print_data(self):
        print self.name, "has",  self.num_centers(), "centers:", self.centers
