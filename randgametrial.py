from board import Board
from actions import Action, Hold, Move, Convoy, Support, Retreat

import random
from datetime import datetime

class RandGameTrial:
    def __init__(self, board, year):
        self.board = board
        self.players = self.board.get_players()
        self.year = year

    def play(self):
        while True:
            self.board.update_centers()
            winner = self.board.get_winner()
            
            if winner != None:
                return winner 

            if self.year > 5000:
                return None

            self.play_build({}, None)

            self.play_moves({}, {}, {}, {}, None)

            self.play_moves({}, {}, {}, {}, None)
            
            self.year += 1

    def play_build(self, builds, ai):
        random.seed(datetime.now())
        random.shuffle(self.players)

        for player in self.players:
            if player != ai:
                builds[player] = self.board.get_all_rand_builds(player)[player]
        
        self.board.auto_execute_builds(builds)

    def play_moves(self, holds, moves, convoys, supports, ai):
        random.shuffle(self.players)

        for player in self.players:
            if player != ai:
                player_holds, player_moves, player_convoys, player_supports = self.board.get_all_rand_actions(player)

                holds.update(player_holds)
                moves.update(player_moves)
                convoys.update(player_convoys)
                supports.update(player_supports)

        retreat_locs = self.board.auto_execute_actions(holds, moves, convoys, supports)

        self.play_retreats(retreat_locs, {}, None)

    def play_retreats(self, retreat_locs, retreats, ai):
        if len(retreat_locs.keys()) != 0:
            random.shuffle(self.players)

            for player in self.players:
                if player != ai:
                    retreats[player] = self.board.get_all_rand_retreats(player)[player]

            self.board.auto_execute_retreats(retreats)
