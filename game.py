from board import Board

class Game:
    def __init__(self, boardfile):
        self.board = Board(boardfile)
        self.year = 1900

    def play(self):
        print "Welcome to Diplomacy! Good luck."

        while True:
            self.board.update_centers()
            winner = self.board.get_winner()
            
            if winner != None:
                print winner, "wins!"
                
                return 

            print "It is winter", self.year - 1
            self.play_build()

            print "It is spring", self.year
            self.play_moves()

            print "It is fall", self.year
            self.play_moves()

            self.year += 1

    def play_build(self):
        builds, messages = self.board.get_builds()

        for message in messages:
            print message

        filename = raw_input("Please enter a build file: ")
        self.board.execute_builds(filename)

        print ""
        self.board.print_players()
        print ""

    def play_moves(self):
        filename = raw_input("Please enter a moves file: ")
        retreat_locs = self.board.execute_actions(filename)

        print ""
        self.board.print_players()
        print ""
        for player_retreat in retreat_locs.keys():
            print player_retreat, "has a retreat at", retreat_locs[player_retreat]
        print ""

        if len(retreat_locs.keys()) != 0:
            filename = raw_input("Please enter a retreat file: ")
            self.board.execute_retreats(filename)

            print ""
            self.board.print_players()
            print ""
