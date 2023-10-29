class GameTracker:
    def __init__(self):
        self.moves = [[" ", " "]]
        self.captured = {"white": [], "black": []}
        self.points = {"white": 0, "black": 0}
        self.turn = "white"
        self.turn_number = 0

    def change_turn(self):
        """other color's turn"""
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
            self.turn_number += 1

    def update_record(self, piece, symbol, to):
        """whose turn and turn number"""
        notation = f"{piece}{symbol}{to}"
        if self.moves[-1][0] == " ":
            self.moves[-1][0] = notation
        elif self.moves[-1][1] == " ":
            self.moves[-1][1] = notation
        if self.moves[-1][0] != " " and self.moves[-1][1] != " ":
            self.moves.append([" ", " "])
        self.change_turn()

    def show_captured_pieces(self):
        """get captured pieces and total points"""
        for color in self.captured.keys():
            print(
                f"{color} ({self.points[color]}){' '*(2-len(str(self.points[color])))}: {''.join(self.captured[color])}"
            )
        print("    ---------------------")

    def show_move_history(self):
        """show all moves made in game"""
        print("    WHITE     |     BLACK")
        print("    ---------------------")
        for pair in self.moves:
            print(
                f"{self.moves.index(pair)+1}."
                f"{' '*(3-len(str(self.moves.index(pair)+1)))}"
                f"{pair[0]}{' '*(10-len(pair[0]))}|"
                f"{' '*(10-len(pair[1]))}{pair[1]}"
            )
        print("    ---------------------")
