from board import Board
from actions import Action, Hold, Move, Convoy, Support, Retreat

import random
from datetime import datetime

class RandGame:
    def __init__(self, boardfile):
        self.board = Board(boardfile)
        self.players = self.board.get_players()
        self.year = 1900

    def play(self):
        print "Welcome to Diplomacy! Good luck."

        while True:
            self.board.update_centers()
            winner = self.board.get_winner()
            
            if winner != None:
                print winner, "wins! Year:", self.year
                
                return 

            if self.year > 5000:
                print "Took too long! Year:", self.year
                return

            #print "It is winter", self.year - 1
            self.play_build()

            #print "It is spring", self.year
            self.play_moves()

            #print "It is fall", self.year
            self.play_moves()
            
            self.year += 1

    def play_build(self):
        builds = {}

        random.seed(datetime.now())
        random.shuffle(self.players)

        for player in self.players:
            builds[player] = self.board.get_all_rand_builds(player)[player]
        
        self.board.auto_execute_builds(builds)

    def play_moves(self):
        holds = {}
        moves = {}
        convoys = {}
        supports = {}

        random.shuffle(self.players)

        for player in self.players:
            player_holds, player_moves, player_convoys, player_supports = self.board.get_all_rand_actions(player)

            holds.update(player_holds)
            moves.update(player_moves)
            convoys.update(player_convoys)
            supports.update(player_supports)

        retreat_locs = self.board.auto_execute_actions(holds, moves, convoys, supports)

        self.play_retreats(retreat_locs, {})

    def play_retreats(self, retreat_locs, retreats):
        if len(retreat_locs.keys()) != 0:
            random.shuffle(self.players)

            for player in self.players:
                retreats[player] = self.board.get_all_rand_retreats(player)[player]
