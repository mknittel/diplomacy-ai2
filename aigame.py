from board import Board
from randgametrial import RandGameTrial
from actions import Action, Hold, Move, Convoy, Support, Retreat
from copy import deepcopy

import random
from datetime import datetime

class AIGame:
    def __init__(self, boardfile, ai):
        self.board = Board(boardfile)
        self.players = self.board.get_players()
        self.year = 1900
        
        #random.seed(datetime.now())
        #index = random.randint(0, len(self.players) - 1)

        self.ai = ai #self.players[index]
        self.players.remove(self.ai)

        self.nnext = 20
        self.ntrials = 400

    def play(self):
        while True:
            print self.year

            self.board.update_centers()
            winner = self.board.get_winner()
            
            if winner != None:
                return winner, self.year

            if self.year > 3000:
                return None, self.year

            self.play_build()

            self.play_moves(True)

            self.play_moves(False)
            
            self.year += 1

    def play_build(self):
        build_set = []
       
        for i in range(0, self.nnext):
            builds = {}
            builds[self.ai] = self.board.get_all_rand_builds(self.ai)[self.ai]
            build_set.append([builds, 0, 0])

        for i in range(0, self.ntrials):
            random.seed(datetime.now())
            index = random.randint(0, self.nnext - 1)

            build = deepcopy(build_set[index][0])
            board = deepcopy(self.board)

            game = RandGameTrial(board, self.year + 1)
            game.play_build(build, self.ai)
            game.play_moves({}, {}, {}, {}, None)
            game.play_moves({}, {}, {}, {}, None)
            winner = game.play()

            if winner != None:
                build_set[index][1] += 1

            if winner == self.ai:
                build_set[index][2] += 1

        index = 0

        for i in range(0, self.nnext):
            if build_set[index][1] == 0:
                index = i
            elif build_set[i][1] != 0:
                this_score = (1.0 * build_set[i][2]) / build_set[i][1]
                best_score = (1.0 * build_set[index][2]) / build_set[index][1]

                if this_score > best_score:
                    index = i

        builds = build_set[index][0]

        random.seed(datetime.now())
        random.shuffle(self.players)

        for player in self.players:
            builds[player] = self.board.get_all_rand_builds(player)[player]


        self.board.auto_execute_builds(builds)

    def play_moves(self, is_spring):
        action_set = []

        for i in range(0, self.nnext):
            holds, moves, convoys, supports = self.board.get_all_rand_actions(self.ai)
            action_set.append([holds, moves, convoys, supports, 0, 0])

        for i in range(0, self.ntrials):
            random.seed(datetime.now())
            index = random.randint(0, self.nnext - 1)

            holds = deepcopy(action_set[index][0])
            moves = deepcopy(action_set[index][1])
            convoys = deepcopy(action_set[index][2])
            supports = deepcopy(action_set[index][3])

            board = deepcopy(self.board)
            game = RandGameTrial(board, self.year + 1)
            game.play_moves(holds, moves, convoys, supports, self.ai)

            if is_spring:
                game.play_moves({}, {}, {}, {}, None)

            winner = game.play()

            if winner != None:
                action_set[index][4] += 1

            if winner == self.ai:
                action_set[index][5] += 1

        index = 0

        for i in range(0, self.nnext):
            if action_set[index][4] == 0:
                index = i
            elif action_set[i][4] != 0:
                this_score = (1.0 * action_set[i][5]) / action_set[i][4]
                best_score = (1.0 * action_set[index][5]) / action_set[index][4]

                if this_score > best_score:
                    index = i

        holds = action_set[index][0]
        moves = action_set[index][1]
        convoys = action_set[index][2]
        supports = action_set[index][3]

        random.shuffle(self.players)

        for player in self.players:
            player_holds, player_moves, player_convoys, player_supports = self.board.get_all_rand_actions(player)

            holds.update(player_holds)
            moves.update(player_moves)
            convoys.update(player_convoys)
            supports.update(player_supports)


        retreat_locs = self.board.auto_execute_actions(holds, moves, convoys, supports)

        self.play_retreats(retreat_locs, is_spring)

    def play_retreats(self, retreat_locs, is_spring):
        if len(retreat_locs.keys()) != 0:
            retreat_set = []

            for i in range(0, self.nnext):
                retreats = {}
                retreats[self.ai] = self.board.get_all_rand_retreats(self.ai)[self.ai]
                retreat_set.append([retreats, 0, 0])

            for i in range(0, self.ntrials):
                random.seed(datetime.now())
                index = random.randint(0, self.nnext - 1)

                retreats = deepcopy(retreat_set[index][0])

                board = deepcopy(self.board)
                game = RandGameTrial(board, self.year + 1)
                game.play_retreats(retreat_locs, retreats, is_spring)

                if is_spring:
                    game.play_moves({}, {}, {}, {}, is_spring)

                winner = game.play()

                if winner != None:
                    retreat_set[index][1] += 1

                if winner == self.ai:
                    retreat_set[index][2] += 1

            index = 0

            for i in range(0, self.nnext):
                if retreat_set[index][1] == 0:
                    index = i
                elif retreat_set[i][1] != 0:
                    this_score = (1.0 * retreat_set[i][2]) / retreat_set[i][1]
                    best_score = (1.0 * retreat_set[index][2]) / retreat_set[index][1]

                    if this_score > best_score:
                        index = i

            retreats = retreat_set[index][0]

            random.shuffle(self.players)

            for player in self.players:
                retreats[player] = self.board.get_all_rand_retreats(player)[player]

            self.board.auto_execute_retreats(retreats)
