import GameTracker, Pieces, Assets

# TODO: check check
# TODO: checkmate check

class Board:
    def __init__(self):
        self.board = self.create_board()
        self.create_pieces()
        self.gt = GameTracker.GameTracker()
        self.show_board()

    ########## SETUP ##########
    def create_board(self):
        """create blank board"""
        board = {}
        for square in Assets.VALID_SQUARES:
            board[square] = Assets.BLANK
        return board

    def create_pieces(self):
        """populate board for new game"""
        for col in Assets.COLS:
            self.board[f"{col}2"] = "♙"
            self.board[f"{col}7"] = "♟"
        for col in "ah":
            self.board[f"{col}1"] = "♖"
            self.board[f"{col}8"] = "♜"
        for col in "bg":
            self.board[f"{col}1"] = "♘"
            self.board[f"{col}8"] = "♞"
        for col in "cf":
            self.board[f"{col}1"] = "♗"
            self.board[f"{col}8"] = "♝"
        for col in "d":
            self.board[f"{col}1"] = "♕"
            self.board[f"{col}8"] = "♛"
        for col in "e":
            self.board[f"{col}1"] = "♔"
            self.board[f"{col}8"] = "♚"

    ######## VISUALIZE ########
    def show_board(self):
        """print current board layout"""
        for i in Assets.ROWS[::-1]:
            print(
                f"{i} |"
                f"{self.board[f'a{i}']}|"
                f"{self.board[f'b{i}']}|"
                f"{self.board[f'c{i}']}|"
                f"{self.board[f'd{i}']}|"
                f"{self.board[f'e{i}']}|"
                f"{self.board[f'f{i}']}|"
                f"{self.board[f'g{i}']}|"
                f"{self.board[f'h{i}']}|"
            )
        print(
            f"{Assets.BLANK*2}a{Assets.BLANK}b{Assets.BLANK}c{Assets.BLANK}d{Assets.BLANK}e{Assets.BLANK}f{Assets.BLANK}g{Assets.BLANK}h"
        )

    ########## LOGIC ##########
    def is_square_valid(self, square):
        """is square found on standard chess board"""
        return (
            len(square) == 2 and square[0] in Assets.COLS and square[1] in Assets.ROWS
        )

    def is_piece_in_square(self, square):
        """does selected square contain a piece"""
        if self.board[square] != Assets.BLANK:
            return True
        else:
            print("blank square")
            return False

    def is_legal_move(self, start, end):
        """is the desired path allowed by this piece
        logic for indivual pieces handled in Pieces.py"""
        return Pieces.PIECES[self.board[start]].move(start, end)

    def get_direction_orthogonal(self, start, end):
        """what direction (U,D,L,R) does the piece want to move"""
        # start == end
        if start[0] == end[0] and start[1] == end[1]:
            return [0, 0]  # should be invalid
        # vertical
        elif start[0] == end[0] and start[1] != end[1]:
            return [0, 1 if int(end[1]) > int(start[1]) else -1]
        # horizontal
        elif start[0] != end[0] and start[1] == end[1]:
            return [
                1 if Assets.COLS.index(end[0]) > Assets.COLS.index(start[0]) else -1,
                0,
            ]

    def get_direction_diagonal(self, start, end):
        """what direction (UL,UR,DL,DR) does the piece want to move"""
        if start[0] != end[0] and start[1] != end[1]:
            # get distance between points
            a = Assets.COLS.index(end[0]) - Assets.COLS.index(start[0])
            b = int(end[1]) - int(start[1])
            # if end directly diagonal from start
            if abs(a) == abs(b):
                return [1 if a > 0 else -1, 1 if b > 0 else -1]

    def is_clear_path(self, start, end):
        """is moving piece blocked"""
        # because knight doesn't follow linear path
        if Pieces.PIECES[self.board[start]].type == "N":
            return True
        else:
            squares_in_path = []
            # orthogonal
            if start[0] == end[0] or start[1] == end[1]:
                direction = self.get_direction_orthogonal(start, end)

                # vertical
                if direction[1] == 0:
                    for i in range(
                        1, abs(Assets.COLS.index(start[0]) - Assets.COLS.index(end[0]))
                    ):
                        square = f"{Assets.COLS[Assets.COLS.index(start[0])+(i*direction[0])]}{int(start[1])}"
                        if self.board[square] != Assets.BLANK:
                            squares_in_path.append(square)
                # horizontal
                elif direction[0] == 0:
                    for i in range(1, abs(int(end[1]) - int(start[1]))):
                        square = f"{start[0]}{int(start[1])+(i*direction[1])}"
                        if self.board[square] != Assets.BLANK:
                            squares_in_path.append(square)
            # diagonal
            else:
                direction = self.get_direction_diagonal(start, end)
                # up
                if direction[1] == 1:
                    for i in range(1, int(end[1]) - int(start[1]) + 1):
                        square = f"{Assets.COLS[Assets.COLS.index(start[0])+(i*direction[0])]}{int(start[1])+(i*direction[1])}"
                        if self.board[square] != Assets.BLANK:
                            squares_in_path.append(square)
                # down
                elif direction[1] == -1:
                    for i in reversed(range(1, int(end[1]) - int(start[1]) + 1, 1)):
                        square = f"{Assets.COLS[Assets.COLS.index(start[0])+(i*direction[0])]}{int(start[1])+(i*direction[1])}"
                        if self.board[square] != Assets.BLANK:
                            squares_in_path.append(square)
            # prevents error of finding moving piece or target piece
            if start in squares_in_path:
                squares_in_path.remove(start)
            if end in squares_in_path:
                squares_in_path.remove(end)
            return True if len(squares_in_path) == 0 else False

    def is_color_turn(self, start):
        """allows only move white piece if white turn, etc."""
        return self.gt.turn == Pieces.PIECES[self.board[start]].color

    # ~#~#~#~#~#~#~#~#~#~#~#~#~#
    def friend_in_end(self):
        """if friendly piece in target square"""
        print("Error, friend found")

    def add_piece_to_captured_dict(self, end):
        """record captured piece in GameTracker.py"""
        n = "white" if self.gt.turn == "black" else "black"
        self.gt.captured[n] += self.board[end]
        self.add_points(end)

    def add_points(self, end):
        """record points in GameTracker.py"""
        n = "white" if self.gt.turn == "black" else "black"
        self.gt.points[n] += Assets.POINT_VALUES[self.board[end]]

    def enemy_in_end(self, start, end):
        """if enemy piece in target square"""
        if Pieces.PIECES[self.board[start]].type == "P":
            # Pawn notation different
            self.gt.update_record(start[0], "x", end)
        else:
            self.gt.update_record(Pieces.PIECES[self.board[start]].type, "x", end)
        # capture
        self.add_piece_to_captured_dict(end)
        self.board[end] = self.board[start]
        self.board[start] = Assets.BLANK

    def move(self, start, end):
        """if no pieces in target square"""
        if Pieces.PIECES[self.board[start]].type == "P":
            # Pawn notation different
            self.gt.update_record("", "", end)
        else:
            self.gt.update_record(Pieces.PIECES[self.board[start]].type, "", end)
        # move
        self.board[end] = self.board[start]
        self.board[start] = Assets.BLANK

    def can_promote(self, end, new_piece):
        """promote pawn if able"""
        if self.board[end] == "♙" and end[1] == "8":
            if new_piece in Assets.WHITE.keys():
                self.board[end] = Assets.WHITE[new_piece]
                self.declare_pawn_promotion(new_piece)
        elif self.board[end] == "♟" and end[1] == "1":
            if new_piece in Assets.BLACK.keys():
                self.board[end] = Assets.BLACK[new_piece]
                self.declare_pawn_promotion(new_piece)

    def end_square_contents(self, start, end, new_piece):
        """decide action based on contents of target square"""
        if self.board[end] != Assets.BLANK:
            if (
                self.board[start] in Pieces.Assets.WHITE.keys()
                and self.board[end] in Pieces.Assets.WHITE.keys()
                or self.board[start] in Pieces.Assets.BLACK.keys()
                and self.board[end] in Pieces.Assets.BLACK.keys()
            ):
                self.friend_in_end()
            else:
                # lets pawn only attack on diagonals
                if Pieces.PIECES[self.board[start]].type == "P" and start[0] == end[0]:
                    self.friend_in_end()
                else:
                    self.enemy_in_end(start, end)
                    self.can_promote(end, new_piece)
        else:
            self.move(start, end)
            self.can_promote(end, new_piece)

    # ~#~#~#~#~#~#~#~#~#~#~#~#~#
    def q_castle_check(self):
        """checks conditions and updates board for king-side castling"""
        color = 1 if self.gt.turn == "white" else 8
        if Pieces.PIECES[self.board[f"a{color}"]].type == "C":
            if (
                self.board[f"b{color}"]
                == self.board[f"c{color}"]
                == self.board[f"d{color}"]
                == Assets.BLANK
            ):
                if Pieces.PIECES[self.board[f"e{color}"]].type == "K":
                    self.board[f"c{color}"] = self.board[f"e{color}"]
                    self.board[f"d{color}"] = self.board[f"a{color}"]
                    self.board[f"a{color}"] = self.board[f"e{color}"] = Assets.BLANK
                    self.gt.update_record("000", "", "")

    def k_castle_check(self):
        """checks conditions and updates board for queen-side castling"""
        color = 1 if self.gt.turn == "white" else 8
        if Pieces.PIECES[self.board[f"h{color}"]].type == "C":
            if self.board["f1"] == self.board[f"g{color}"] == Assets.BLANK:
                if Pieces.PIECES[self.board[f"e{color}"]].type == "K":
                    self.board[f"g{color}"] = self.board[f"e{color}"]
                    self.board[f"f{color}"] = self.board[f"h{color}"]
                    self.board[f"h{color}"] = self.board[f"e{color}"] = Assets.BLANK
                    self.gt.update_record("00", "", "")

    def declare_check(self):
        """adds + to notation"""
        self.gt.moves[
            -2 if self.gt.moves[-1][0] == self.gt.moves[-1][1] == " " else -1
        ][1 if self.gt.turn == "white" else 0] += "+"

    def declare_check_mate(self):
        """adds ++ to notation"""
        self.gt.moves[
            -2 if self.gt.moves[-1][0] == self.gt.moves[-1][1] == " " else -1
        ][1 if self.gt.turn == "white" else 0] += "++"

    def declare_pawn_promotion(self, new_piece="Q"):
        """adds =new_piece to notation"""
        self.gt.moves[
            -2 if self.gt.moves[-1][0] == self.gt.moves[-1][1] == " " else -1
        ][1 if self.gt.turn == "white" else 0] += f"={new_piece}"

    def declare_resign(self):
        """adds RESIGN to notation"""
        self.gt.moves[-1][0 if self.gt.turn == "white" else 1] = "RESIGN"

    ######## MOVE PIECE #######
    def move_piece(self, start, end, new_piece=None):
        if start == "000":
            self.q_castle_check()
        elif start == "00":
            self.k_castle_check()
        elif start == "++":
            self.declare_check_mate()
        else:
            if self.is_square_valid(start):
                if self.is_piece_in_square(start):
                    if self.is_color_turn(start):
                        if self.is_square_valid(end):
                            if self.is_legal_move(start, end):
                                if self.is_clear_path(start, end):
                                    self.end_square_contents(start, end, new_piece)


    def test_game(self):
        # https://www.mathsisfun.com/games/chess.html
        # https://www.family-games-treasurehouse.com/sample_chess_game.html

        self.move_piece('e2', 'e4'), self.move_piece('e7', 'e5')
        self.move_piece('g1', 'f3'), self.move_piece('d7', 'd6')
        self.move_piece('d2', 'd4'), self.move_piece('c8', 'g4')
        self.move_piece('d4', 'e5'), self.move_piece('g4', 'f3')
        self.move_piece('d1', 'f3'), self.move_piece('d6', 'e5')
        self.move_piece('f1', 'c4'), self.move_piece('g8', 'f6')
        self.move_piece('f3', 'b3'), self.move_piece('d8', 'e7')
        self.move_piece('b1', 'c3'), self.move_piece('c7', 'c6')
        self.move_piece('c1', 'g5'), self.move_piece('b7', 'b5')
        self.move_piece('c3', 'b5'), self.move_piece('c6', 'b5')
        self.move_piece('c4', 'b5'), self.declare_check(), self.move_piece('b8', 'd7')
        self.move_piece('000', '-'), self.move_piece('a8', 'd8')
        self.move_piece('d1', 'd7'), self.declare_check(), self.move_piece('d8', 'd7')
        self.move_piece('h1', 'd1'), self.move_piece('e7', 'e6')
        self.move_piece('b5', 'd7'), self.move_piece('f6', 'd7')
        self.move_piece('b3', 'b8'), self.declare_check(), self.move_piece('d7', 'b8')
        self.move_piece('d1', 'd8'), self.declare_check_mate()

    def test_game_2(self):
        # https://www.chessgames.com/perl/chessgame?gid=1075465

        self.move_piece('e2', 'e4'), self.move_piece('e7', 'e5')
        self.move_piece('f2', 'f4'), self.move_piece('e5', 'f4')
        self.move_piece('f1', 'c4'), self.move_piece('d8', 'h4'), self.declare_check()
        self.move_piece('e1', 'f1'), self.move_piece('g7', 'g5')
        self.move_piece('b1', 'c3'), self.move_piece('f8', 'g7')

        self.move_piece('d2', 'd4'), self.move_piece('d7', 'd6')
        self.move_piece('c3', 'd5'), self.move_piece('e8', 'd8')
        self.move_piece('c4', 'e2'), self.move_piece('b8', 'c6')
        self.move_piece('e4', 'e5'), self.move_piece('g8', 'e7')
        self.move_piece('d5', 'c3'), self.move_piece('e7', 'f5')

        self.move_piece('g1', 'f3'), self.move_piece('h4', 'h6')
        self.move_piece('c3', 'e4'), self.move_piece('f7', 'f6')
        self.move_piece('e5', 'f6'), self.move_piece('g7', 'f6')
        self.move_piece('g2', 'g4'), self.move_piece('f5', 'd4')
        self.move_piece('f1', 'g2'), self.move_piece('c8', 'g4')

        self.move_piece('h2', 'h4'), self.move_piece('g4', 'f3'), self.declare_check()
        self.move_piece('e2', 'f3'), self.move_piece('d4', 'f3')
        self.move_piece('d1', 'f3'), self.move_piece('c6', 'e5')
        self.move_piece('f3', 'b3'), self.move_piece('h6', 'g6')
        self.move_piece('b3', 'b7'), self.move_piece('a8', 'c8')

        self.move_piece('c1', 'd2'), self.move_piece('g5', 'h4'), self.declare_check()
        self.move_piece('g2', 'f1'), self.move_piece('h8', 'g8')
        self.move_piece('e4', 'd6'), self.move_piece('c7', 'd6')
        self.move_piece('d2', 'a5'), self.declare_check(), self.move_piece('d8', 'e8')
        self.move_piece('b7', 'c8'), self.declare_check(), self.move_piece('e8', 'f7')

        self.move_piece('c8', 'b7'), self.declare_check(), self.move_piece('f6', 'e7')
        self.move_piece('b7', 'd5'), self.declare_check(), self.move_piece('f7', 'f8')
        self.move_piece('a1', 'd1'), self.move_piece('f4', 'f3')
        self.move_piece('d1', 'd2'), self.move_piece('h4', 'h3')
        self.move_piece('d5', 'a8'), self.declare_check(), self.move_piece('f8', 'f7')

        self.move_piece('a8', 'd5'), self.declare_check(), self.move_piece('f7', 'f8')
        self.move_piece('d5', 'a8'), self.declare_check(), self.move_piece('f8', 'g7')
        self.move_piece('a8', 'a7'), self.move_piece('g6', 'g2'), self.declare_check()
        self.move_piece('d2', 'g2'), self.declare_check(), self.move_piece('f3', 'g2'), self.declare_check()
        self.move_piece('f1', 'g1'), self.move_piece('e5', 'f3'), self.declare_check()

        self.move_piece('g1', 'f2'), self.move_piece('g2', 'h1'), self.can_promote('h1', 'Q')
        self.move_piece('a7', 'e7'), self.declare_check(), self.move_piece('g7', 'h6')
        self.move_piece('e7', 'd6'), self.declare_check(), self.move_piece('h6', 'h5')
        self.move_piece('d6', 'd5'), self.declare_check(), self.move_piece('g8', 'g5')
        self.move_piece('d5', 'f7'), self.declare_check(), self.move_piece('h5', 'g4')

        self.move_piece('f7', 'c4'), self.declare_check(), self.move_piece('f3', 'd4')
        self.move_piece('c4', 'd4'), self.declare_check(), self.move_piece('g4', 'h5')
        self.move_piece('a5', 'b6'), self.move_piece('h1', 'h2'), self.declare_check()
        self.move_piece('f2', 'e1'), self.move_piece('g5', 'e5'), self.declare_check()
        self.move_piece('e1', 'd1'), self.move_piece('h2', 'e2'), self.declare_check()

        self.move_piece('d1', 'c1'), self.move_piece('e2', 'e1'), self.declare_check()
        self.move_piece('d4', 'd1'), self.declare_check(), self.move_piece('e1', 'd1'), self.declare_check()
        self.move_piece('c1', 'd1'), self.move_piece('h3', 'h2')
        self.declare_resign()