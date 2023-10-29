# chess

This is a fully playable chess game that uses a text-based interface like below. (Everything is aligned on my computer but it might not be for yours)

8 |♜|♞|♝|♛|♚|♝|♞|♜|

7 |♟|♟|♟|♟|♟|♟|♟|♟|

6 |  |  |  |  |  |  |  |  |

5 |  |  |  |  |  |  |  |  |

4 |  |  |  |  |  |  |  |  |

3 |  |  |  |  |  |  |  |  |

2 |♙|♙|♙|♙|♙|♙|♙|♙|

1 |♖|♘|♗|♕|♔|♗|♘|♖|

   a  b  c  d  e f  g  h

HOW TO USE
1. Download and place all files in the same place
2. Run 'Chess.py'
3. Enter a command to play the game

COMMANDS
quit  -> you resign
score -> get the current score based on pieces captured, and a list of said pieces
moves -> get a list of all moves played in the current game in standard chess notation
00    -> king-side castle
000   -> queen-side castle
a1b2C -> move the piece in square 'a1' to square 'b2'. If it is a pawn reaching the end row, promote it to piece type 'C'
