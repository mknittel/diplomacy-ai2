class Action:
    def __init__(self, start, player):
        self.start = start
        self.player = player

    def print_action(self):
        print "Action on", self.start, "by", self.player

class Hold(Action):
    def __init__(self, start, player):
        Action.__init__(self, start, player)

    def print_action(self):
        print "Hold at", self.start, "by", self.player

class Move(Action):
    def __init__(self, start, dest, player):
        self.dest = dest
        Action.__init__(self, start, player)

    def print_action(self):
        print "Move from", self.start, "to", self.dest, "by", self.player

class Convoy(Action):
    def __init__(self, start, dest, convoys, player):
        self.dest = dest
        self.convoys = convoys
        Action.__init__(self, start, player)

    def print_action(self):
        print "Convoy from", self.start, "to", self.dest, "via", self.convoys, "by", self.player

class Support:
    def __init__(self, loc, action, player):
        self.loc = loc
        self.action = action
        self.player = player

    def print_action(self):
        print "Action by", self.player, "at", self.loc, "supports:"

        self.action.print_action()
