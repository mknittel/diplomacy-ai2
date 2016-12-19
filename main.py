from game import Game
from aigame import AIGame
from board import Board
from randgame import RandGame

def main():
    for i in range(0, 100):
        game = AIGame("europe.txt")
        win = game.play()
        ai = game.ai

        if win == ai:
            print "AI won as", ai
        elif win != None:
            print "AI lost as", ai, "and", win, "won."
        else:
            print "Game timed out."

if __name__ == "__main__":
    main()
