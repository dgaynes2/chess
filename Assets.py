# board layout
COLS = "abcdefgh"
ROWS = "12345678"
VALID_SQUARES = [f"{col}{row}" for col in COLS for row in ROWS]
BLANK = "   "

# piece info
PIECE_ABBRS = "KQBNCP"
WHITE = {'C':"♖",'N':"♘",'B':"♗",'Q':"♕"}
BLACK = {'C':"♜",'N':"♞",'B':"♝",'Q':"♛"}
POINT_VALUES = {"♙": 1,"♟": 1,"♗": 3,"♝": 3,"♘": 3,"♞": 3,"♖": 5,"♜": 5,"♕": 9,"♛": 9,}
