import Board, GameTracker, Pieces, re


class Game:
    def __init__(self):
        self.running = True
        self.board = Board.Board()
        self.pattern = "^(0{2,3}$)|(([a-h][1-8]){2}(Q|N|B|C)?$)"

    def move_parse(self, move):
        if len(move) == 2 or len(move) == 3:
            self.board.move_piece(move[:], "")
        elif len(move) == 4:
            self.board.move_piece(move[0:2], move[2:4])
        elif len(move) == 5:
            self.board.move_piece(move[0:2], move[2:4], move[4])

    def run(self):
        while self.running:
            move = input("MOVE: ")

            if move.strip() == "":
                continue
            if move.lower() in ["quit", "forfeit", "give up", "resign"]:
                print(f"{self.board.gt.turn.upper()} resigns")
                self.running = False
            elif move.lower() in ["score", "captured"]:
                self.board.gt.show_captured_pieces()
            elif move.lower() == "moves":
                self.board.gt.show_move_history()
            else:
                if re.match(self.pattern, move):
                    self.move_parse(move)
                    self.board.show_board()


if __name__ == "__main__":
    g = Game()
    g.run()
