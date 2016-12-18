import prolog1 as prolog

from actions import Action
from actions import Hold
from actions import Move
from actions import Convoy
from actions import Support

class Resolver:
    def __init__(self, players, provinces, holds, moves, convoys, supports):
        self.players = players
        self.provinces = provinces
        self.holds = holds
        self.moves = moves
        self.convoys = convoys
        self.supports = supports

    def resolve_moves(self):
        
