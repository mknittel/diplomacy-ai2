from actions import Action, Hold, Move, Convoy, Support, Retreat

class Parser:
    def __init__(self):
        self.holds = {}
        self.moves = {}
        self.convoys = {}
        self.supports = {}

    def restart(self):
        self.holds.clear()
        self.moves.clear()
        self.convoys.clear()
        self.supports.clear()

    def read_board(self, filename):
        f = open(filename, 'r')
        players = []
        land_provinces = []
        sea_provinces = []
        coasts = []
        centers = []
        mode = ""

        for line in f:
            line = line[:-1]
            words = line.split(", ")

            if line != "-":
                if mode == "player":
                    players += [words]
                elif mode == "land":
                    land_provinces += [words]
                elif mode == "sea":
                    sea_provinces += [words]
                elif mode == "coasts":
                    coasts += [words]
                elif mode == "centers":
                    centers += [words]
            else:
                mode = ""
                
            if line == "Players:":
                mode = "player"
            elif line == "Land provinces:":
                mode = "land"
            elif line == "Sea provinces:":
                mode = "sea"
            elif line == "Coasts:":
                mode = "coasts"
            elif line == "Centers:":
                mode = "centers"
        
        f.close()

        return players, land_provinces, sea_provinces, coasts, centers

    def read_builds(self, filename):
        f = open(filename, 'r')
        player = ""
        builds = {}

        for line in f:
            line = line[:-1]
            words = line.split(" ")

            if line != "-":
                if player != "" and player not in builds.keys():
                    builds[player] = [words]
                elif player != "":
                    builds[player].append(words)
                else:
                    player = line
            else:
                player = ""

        f.close()

        return builds

    def read_retreats(self, filename):
        f = open(filename, 'r')
        player = ""
        retreats = {}

        for line in f:
            line = line[:-1]
            words = line.split(" ")
            
            if line != "-":
                if player != "" and player not in retreats.keys():
                    retreats[player] = [words]
                elif player != "":
                    retreats[player].append(words)
                else:
                    player = line
            else:
                player = ""
        
        f.close()

        return retreats

    def read_actions(self, filename):
        f = open(filename, 'r')
        player = ""

        for line in f:
            line = line[:-1]
            words = line.split(" ")

            if line != "-":
                if player != "":
                    self.make_action(words)
                else:
                    player = line
            else:
                player = ""

        f.close()

    def get_actions(self):
        return self.holds, self.moves, self.convoys, self.supports

    def make_action(self, words):
        act = words[2]
        loc = words[1]

        if act == "hold":
            hold = Hold(loc)
            self.holds[loc] = hold
        elif act == "to":
            move = Move(loc, words[3])
            self.moves[loc] = move
        elif act == "convoy":
            # Can only convoy self
            convoyee = words[4]

            if convoyee in self.convoys:
                convoy = self.convoys[convoyee]
                convoy.convoys.append(loc)
                self.convoys[convoyee] = convoy
            else:
                convoy = Convoy(convoyee, words[6], [loc])
                self.convoys[convoyee] = convoy
        elif act == "support":
            support_act = words[5]
            support_loc = words[4]

            if support_act == "hold":
                if support_loc in self.holds:
                    hold = self.holds[support_loc]
                    support = Support(loc, hold)
                    self.supports[loc] = support
                else:
                    print "Error: invalid hold support", words
            elif support_act == "to":
                if support_loc in self.moves:
                    move = self.moves[support_loc]
                    support = Support(loc, move)
                    self.supports[loc] = support
                else:
                    print "Error: invalid move support", words
            elif support_act == "convoy":
                dest = words[7]

                if dest in self.convoys:
                    convoy = self.convoys[dest]
                    support = Support(loc, convoy)
                    self.supports[loc] = support
                else:
                    print "Error: invalid convoy support:", words
        else:
            print "Error: incorrect move", words
