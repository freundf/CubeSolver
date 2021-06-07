from cube import Piece
from cube_coloring import Color

pieces_solved = (Piece([-1, 1, -1], [state[1][0], state[0][0], state[4][2]]),
                 Piece([0, 1, -1], [None, state[0][1], state[4][1]]),
                 Piece([1, 1, -1], [state[3][2], state[0][2], state[4][0]]),
                 Piece([-1, 1, 0], [state[1][1], state[0][3], Non
                 Piece([0, 1, 0], [None, state[0][4], None]),
                 Piece([1, 1, 0], [state[3][1], state[0][5], None]),
                 Piece([-1, 1, 1], [state[1][2], state[0][6], state[2][0]]),
                 Piece([0, 1, 1], [None, state[0][7], state[2][1]]),
                 Piece([1, 1, 1], [state[3][0], state[0][8], state[2][2]]),

                 Piece([-1, 0, -1], [state[1][3], None, state[4][5]]),
                 Piece([0, 0, -1], [None, None, state[4][4]]),
                 Piece([1, 0, -1], [state[3][5], None, state[4][3]]),
                 Piece([-1, 0, 0], [state[1][4], None, None]),
                 Piece([0, 0, 0], [None, None, None]),
                 Piece([1, 0, 0], [state[3][4], None, None]),
                 Piece([-1, 0, 1], [state[1][5], None, state[2][3]]),
                 Piece([0, 0, 1], [None, None, state[2][4]]),

                 Piece([-1, -1, -1], [state[1][6], state[5][6], state[4][8]]),
                 Piece([0, -1, -1], [None, state[5][7], state[4][7]]),
                 Piece([1, -1, -1], [state[3][8], state[5][8], state[4][6]]),
                 Piece([-1, -1, 0], [state[1][7], state[5][3], None]),
                 Piece([0, -1, 0], [None, state[5][4], None]),
                 Piece([1, -1, 0], [state[3][7], state[5][5], None]),
                 Piece([-1, -1, 1], [state[1][8], state[5][0], state[2][6]]),
                 Piece([0, -1, 1], [None, state[5][1], state[2][7]]),
                 Piece([1, -1, 1], [state[3][6], state[5][2], state[2][8]]))
