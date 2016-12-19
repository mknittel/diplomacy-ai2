class Action:
    def __init__(self, start):
        self.start = start
        self.action_power = 1
        self.hold_power = 1

    def add_power(self):
        self.action_power += 1

    def print_action(self):
        print "Action on", self.start

class Hold(Action):
    def __init__(self, start):
        self.is_hold = True
        self.action_type = "Hold"
        Action.__init__(self, start)

    def print_action(self):
        print "Hold at", self.start

    def add_power(self):
        self.action_power += 1
        self.hold_power += 1

class Move(Action):
    def __init__(self, start, dest):
        self.is_hold = False
        self.dest = dest
        self.action_type = "Move"
        Action.__init__(self, start)

    def print_action(self):
        print "Move from", self.start, "to", self.dest

    def add_power(self):
        self.action_power += 1

class Convoy(Action):
    def __init__(self, start, dest, convoys):
        self.is_hold = False
        self.dest = dest
        self.action_type = "Convoy"
        self.convoys = convoys
        Action.__init__(self, start)

    def print_action(self):
        print "Convoy from", self.start, "to", self.dest, "via", self.convoys

    def add_power(self):
        self.action_power += 1

class Support:
    def __init__(self, loc, action):
        self.loc = loc
        self.action = action
        self.action_type = "Support"

    def print_action(self):
        print "Action at", self.loc, "supports:"

        self.action.print_action()

class Retreat:
    def __init__(self, loc):
        self.loc = loc

    def print_action(self):
        print "Retreat at", self.loc
