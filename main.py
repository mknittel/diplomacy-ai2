from game import Game
from aigame import AIGame
from board import Board
from randgame import RandGame

def main():
    russia = 0
    turkey = 0
    italy = 0
    france = 0
    britain = 0
    germany = 0
    austria_hungary = 0
    none = 0
    sum_yrs = 0

    """

    for i in range(0, 100):
        game = RandGame("map4.txt")
        winner, nyears = game.play()

    """


    for i in range(0, 100):
        game = AIGame("map3.txt", "France")
        winner, nyears = game.play()

        print "Trial:", i

        sum_yrs += nyears - 1900

        if winner == None:
            none += 1
        elif winner == "Russia":
            russia += 1
        elif winner == "Turkey":
            turkey += 1
        elif winner == "Germany":
            germany += 1
        elif winner == "Italy":
            italy += 1
        elif winner == "France":
            france += 1
        elif winner == "Britain":
            britain += 1
        elif winner == "Austria":
            austria_hungary += 1

    print str(russia), str(turkey), str(italy), str(france), str(britain), str(germany), str(austria_hungary), str(none)
    print "Average number of years: ", ((1.0 * sum_yrs) / 100)

if __name__ == "__main__":
    main()
