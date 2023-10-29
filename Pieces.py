import Assets


class Piece:
    def __init__(self, color):
        self.color = color
        self.direction = 1 if color == "black" else -1
        self.type = None

    ####### VALIDITY CHECKS #######
    def same_column(self, start, end):
        return start[0] == end[0]

    def same_row(self, start, end):
        return start[1] == end[1]

    def get_direction_orthogonal(self, start, end):
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
        if start[0] != end[0] and start[1] != end[1]:
            a = Assets.COLS.index(end[0]) - Assets.COLS.index(start[0])
            b = int(end[1]) - int(start[1])
            # if end directly diagonal from end
            if abs(a) == abs(b):
                return [1 if a > 0 else -1, 1 if b > 0 else -1]


class Pawn(Piece):  # ♙♟
    def __init__(self, color):
        super().__init__(color)
        self.type = "P"

    def move(self, start, end):
        # move
        if self.same_column(start, end):
            # 2-square
            if self.get_distance(start, end) * self.direction == -2:
                if self.in_start_row(start):
                    return True
            # normal move
            elif self.get_distance(start, end) * self.direction == -1:
                return True
        else:  # capture
            return True if self.get_capture_squares(start, end) else False

    ####### VALIDITY CHECKS #######
    def get_distance(self, start, end):
        return int(end[1]) - int(start[1])

    def in_start_row(self, start):
        return (
            True
            if (
                start[1] == "2"
                and self.color == "white"
                or start[1] == "7"
                and self.color == "black"
            )
            else False
        )

    def get_capture_squares(self, start, end):
        d = -1 if self.color == "black" else 1
        can_capture_squares = []

        for i in [-1, 1]:
            if Assets.COLS.index(start[0]) + i in range(0, 8):
                can_capture_squares.append(
                    f"{Assets.COLS[Assets.COLS.index(start[0]) + i]}{int(start[1])+d}"
                )
        return True if end in can_capture_squares else False


class Castle(Piece):  # ♖♜
    def __init__(self, color):
        super().__init__(color)
        self.type = "C"

    def move(self, start, end):
        return (
            True
            if (
                self.get_direction_orthogonal(start, end)[0] == 0
                or self.get_direction_orthogonal(start, end)[1] == 0
                and not self.get_direction_orthogonal(start, end)[0]
                == self.get_direction_orthogonal(start, end)[1]
                == 0
            )
            else False
        )


class Knight(Piece):  # ♘♞
    def __init__(self, color):
        super().__init__(color)
        self.type = "N"

    def move(self, start, end):
        return True if self.possible_squares(start, end) else False

    ####### VALIDITY CHECKS #######
    def possible_squares(self, start, end):
        can_go_squares = []

        # get valid columns
        cols = [
            int(Assets.COLS.index(start[0])) + i
            for i in [-2, -1, 1, 2]
            if int(Assets.COLS.index(start[0])) + i in range(0, 8)
        ]
        # get valid rows
        rows = [
            str(int(start[1]) + i)
            for i in [-2, -1, 1, 2]
            if str(int(start[1]) + i) in Assets.ROWS
        ]

        for col in cols:
            for row in rows:
                # get valid squares
                if abs(int(Assets.COLS.index(start[0])) - col) != abs(
                    int(start[1]) - int(row)
                ):
                    can_go_squares.append(f"{Assets.COLS[col]}{row}")
        # True if end square in legal squares
        return True if end in can_go_squares else False


class Bishop(Piece):  # ♗♝
    def __init__(self, color):
        super().__init__(color)
        self.type = "B"

    def move(self, start, end):
        return True if self.get_direction_diagonal(start, end) else False


class Queen(Piece):  # ♕♛
    def __init__(self, color):
        super().__init__(color)
        self.type = "Q"

    def move(self, start, end):
        return (
            True
            if (
                self.same_column(start, end)
                or self.same_row(start, end)
                or self.get_direction_diagonal(start, end)
            )
            else False
        )


class King(Piece):  # ♔♚
    def __init__(self, color):
        super().__init__(color)
        self.type = "K"

    def move(self, start, end):
        return True if self.possible_squares(start, end) else False

    def possible_squares(self, start, end):
        can_go_squares = []

        # get valid columns
        cols = [
            int(Assets.COLS.index(start[0])) + i
            for i in [-1, 0, 1]
            if int(Assets.COLS.index(start[0])) + i in range(0, 8)
        ]
        # get valid rows
        rows = [
            str(int(start[1]) + i)
            for i in [-1, 0, 1]
            if str(int(start[1]) + i) in Assets.ROWS
        ]

        for col in cols:
            for row in rows:
                can_go_squares.append(f"{Assets.COLS[col]}{row}")
        # True if end square in legal squares
        return True if end in can_go_squares else False


WHITE = {
    "♙": Pawn("white"),
    "♖": Castle("white"),
    "♘": Knight("white"),
    "♗": Bishop("white"),
    "♕": Queen("white"),
    "♔": King("white"),
}
BLACK = {
    "♟": Pawn("black"),
    "♜": Castle("black"),
    "♞": Knight("black"),
    "♝": Bishop("black"),
    "♛": Queen("black"),
    "♚": King("black"),
}
PIECES = {**WHITE, **BLACK}
