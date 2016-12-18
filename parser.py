from actions import Action
from actions import Hold
from actions import Move
from actions import Convoy
from actions import Support

class Parser:
    def __init__(self):
        self.holds = {}
        self.moves = {}
        self.convoys = {}
        self.supports = {}

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

    def read_actions(self, filename):
        f = open(filename, 'r')
        player = ""

        for line in f:
            line = line[:-1]
            words = line.split(" ")

            if line != "-":
                if player != "":
                    self.make_action(words, player)
                else:
                    player = line
            else:
                player = ""

        f.close()

    def get_actions(self):
        return self.holds, self.moves, self.convoys, self.supports

    def make_action(self, words, player):
        act = words[2]
        loc = words[1]

        if act == "hold":
            hold = Hold(loc, player)
            self.holds[loc] = hold
        elif act == "to":
            move = Move(loc, words[3], player)
            self.moves[loc] = move
        elif act == "convoy":
            convoyee = words[4]

            if convoyee in self.convoys:
                convoy = self.convoys[convoyee]
                convoy.convoys.append(loc)
                self.convoys[convoyee] = convoy
            else:
                convoy = Convoy(convoyee, words[6], [loc], player)
                self.convoys[convoyee] = convoy
        elif act == "support":
            support_act = words[5]
            support_loc = words[4]

            if support_act == "hold":
                if support_loc in self.holds:
                    hold = self.holds[support_loc]
                    support = Support(loc, hold, player)
                    self.supports[loc] = support
                else:
                    print "Error: invalid hold support", words
            elif support_act == "to":
                if support_loc in self.moves:
                    move = self.moves[support_loc]
                    support = Support(loc, move, player)
                    self.supports[loc] = support
                else:
                    print "Error: invalid move support", words
            elif support_act == "convoy":
                dest = words[7]

                if dest in self.convoys:
                    convoy = self.convoys[dest]
                    support = Support(loc, convoy, player)
                    self.supports[loc] = support
                else:
                    print "Error: invalid convoy support:", words
        else:
            print "Error: incorrect move", words
