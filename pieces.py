from cube import Piece
from constants import Color


pieces_solved = (Piece([-1, 1, -1], [Color(1), Color(0), Color(4)]),
                 Piece([0, 1, -1], [None, Color(0), Color(4)]),
                 Piece([1, 1, -1], [Color(3), Color(0), Color(4)]),
                 Piece([-1, 1, 0], [Color(1), Color(0), None]),
                 Piece([0, 1, 0], [None, Color(0), None]),
                 Piece([1, 1, 0], [Color(3), Color(0), None]),
                 Piece([-1, 1, 1], [Color(1), Color(0), Color(2)]),
                 Piece([0, 1, 1], [None, Color(0), Color(2)]),
                 Piece([1, 1, 1], [Color(3), Color(0), Color(2)]),

                 Piece([-1, 0, -1], [Color(1), None, Color(4)]),
                 Piece([0, 0, -1], [None, None, Color(4)]),
                 Piece([1, 0, -1], [Color(3), None, Color(4)]),
                 Piece([-1, 0, 0], [Color(1), None, None]),
                 Piece([0, 0, 0], [None, None, None]),
                 Piece([1, 0, 0], [Color(3), None, None]),
                 Piece([-1, 0, 1], [Color(1), None, Color(2)]),
                 Piece([0, 0, 1], [None, None, Color(2)]),
                 Piece([1, 0, 1], [Color(3), None, Color(2)]),

                 Piece([-1, -1, -1], [Color(1), Color(5), Color(4)]),
                 Piece([0, -1, -1], [None, Color(5), Color(4)]),
                 Piece([1, -1, -1], [Color(3), Color(5), Color(4)]),
                 Piece([-1, -1, 0], [Color(1), Color(5), None]),
                 Piece([0, -1, 0], [None, Color(5), None]),
                 Piece([1, -1, 0], [Color(3), Color(5), None]),
                 Piece([-1, -1, 1], [Color(1), Color(5), Color(2)]),
                 Piece([0, -1, 1], [None, Color(5), Color(2)]),
                 Piece([1, -1, 1], [Color(3), Color(5), Color(2)]))
