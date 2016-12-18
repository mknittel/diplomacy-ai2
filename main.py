from board import Board

def main():
    board = Board("europe.txt")
    board.execute_actions("moves1.txt")
    board.execute_actions("moves2.txt")

if __name__ == "__main__":
    main()
