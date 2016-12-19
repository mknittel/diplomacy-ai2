from board import Board
from randgametrial import RandGameTrial
from actions import Action, Hold, Move, Convoy, Support, Retreat
from copy import deepcopy

import random
from datetime import datetime

class AIGame:
    def __init__(self, boardfile):
        self.board = Board(boardfile)
        self.players = self.board.get_players()
        self.year = 1900
        
        random.seed(datetime.now())
        index = random.randint(0, len(self.players) - 1)

        self.ai = self.players[index]
        self.players.remove(self.ai)

    def play(self):
        while True:
            self.board.update_centers()
            winner = self.board.get_winner()
            
            if winner != None:
                return winner

            if self.year > 5000:
                return None

            #print "It is winter", self.year - 1
            self.play_build()

            #print "It is spring", self.year
            self.play_moves(True)

            #print "It is fall", self.year
            self.play_moves(False)
            
            self.year += 1

    def play_build(self):
        build_set = []
       
        for i in range(0, 20):
            builds = {}
            builds[self.ai] = self.board.get_all_rand_builds(self.ai)[self.ai]
            build_set.append([builds, 0, 0])

        for i in range(0, 100):
            random.seed(datetime.now())
            index = random.randint(0, 19)

            build = build_set[index][0]
            board = deepcopy(self.board)

            game = RandGameTrial(board, self.year + 1)
            game.play_build(build)
            game.play_moves({}, {}, {}, {})
            game.play_moves({}, {}, {}, {})
            winner = game.play()

            if winner != None:
                build_set[index][1] += 1

            if winner == self.ai:
                build_set[index][2] += 1

        index = 0

        for i in range(0, 20):
            if build_set[index][2] == 0:
                index = i
            elif build_set[i][2] != 0:
                this_score = (1.0 * build_set[i][2]) / build_set[i][1]
                best_score = (1.0 * build_set[index][2]) / build_set[index][1]

                if this_score > best_score:
                    index = i
 
        self.board.auto_execute_builds(build_set[index][0])

    def play_moves(self, is_spring):
        action_set = []

        for i in range(0, 20):
            holds, moves, convoys, supports = self.board.get_all_rand_actions(self.ai)
            action_set.append([holds, moves, convoys, supports, 0, 0])

        for i in range(0, 100):
            random.seet(datetime.now())
            index = random.randint(0, 19)

            holds = action_set[index][0]
            moves = action_set[index][1]
            convoys = action_set[index][2]
            supports = action_set[index][3]

            board = deepcopy(self.board)
            game = RandGameTrial(board, self.year + 1)
            game.play_moves(holds, moves, convoys, supports)

            if is_spring:
                game.play_moves({}, {}, {}, {})

            winner = game.play()

            if winner != None:
                action_set[index][4] += 1

            if winner == self.ai:
                action_set[index][5] += 1

        index = 0

        for i in range(0, 20):
            if action_set[index][2] == 0:
                index = i
            elif action_set[i][2] != 0:
                this_score = (1.0 * action_set[i][5]) / action_set[i][4]
                best_score = (1.0 * action_set[index][5]) / action_set[index][4]

                if this_score > best_score:
                    index = i

        holds = action_set[index][0]
        moves = action_set[index][1]
        convoys = action_set[index][2]
        supports = action_set[index][3]

        retreat_locs = self.board.auto_execute_actions(holds, moves, convoys, supports)

        self.play_retreats(retreat_locs, is_spring)

    def play_retreats(self, retreat_locs, is_spring):
        if len(retreat_locs.keys()) != 0:
            retreat_set = []

            for i in range(0, 20):
                retreats = {}
                retreats[player] = self.board.get_all_rand_retreats(player)[player]
                retreat_set.append([retreats, 0, 0])

            for i in range(0, 100):
                random.seet(datetime.now())
                index = random.randint(0, 19)

                retreats = retreat_set[index][0]

                board = deepcopy(self.board)
                game = RandGameTrial(board, self.year + 1)
                game.play_retreats(retreat_locs, retreats)

                if is_spring:
                    game.play_moves({}, {}, {}, {})

                winner = game.play()

                if winner != None:
                    retreat_set[index][1] += 1

                if winner == self.ai:
                    retreat_set[index][2] += 1

            index = 0

            for i in range(0, 20):
                if aretreat_set[index][2] == 0:
                    index = i
                elif retreat_set[i][2] != 0:
                    this_score = (1.0 * retreat_set[i][2]) / retreat_set[i][1]
                    best_score = (1.0 * retreat_set[index][2]) / retreat_set[index][1]

                    if this_score > best_score:
                        index = i

            self.board.auto_execute_retreats(retreat_set[index][0])
