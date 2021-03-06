from constants import Color, rotations, inverse_rotations, face_to_cubestate
from collections import namedtuple


"""
Cube_state indexes:
                  [0]
              +---------+
              | 0  1  2 |
              | 3  4  5 |
        [1]   | 6  7  8 |   [3]       [4]
    +---------+---------+---------+---------+
    | 0  1  2 | 0  1  2 | 0  1  2 | 0  1  2 |
    | 3  4  5 | 3  4  5 | 3  4  5 | 3  4  5 |
    | 6  7  8 | 6  7  8 | 6  7  8 | 6  7  8 |
    +---------+---------+---------+---------+
            / | 0  1  2 |
           /  | 3  4  5 |
         [2]  | 6  7  8 |
              +---------+
                  [5]
"""
cube_state = [[color] * 9 for color in Color]


face_axis = {
    "F": (1, -1, 0),
    "B": (-1, -1, 0),
    "U": (1, 0, 1),
    "D": (1, 0, -1),
    "R": (0, -1, -1),
    "L": (0, -1, 1),
}

face_encoding = {
    "F": [0, 1],
    "B": [0, 1],
    "U": [0, 2],
    "D": [0, 2],
    "R": [2, 1],
    "L": [2, 1],
}

color_swaps = {
    0: (0, 2, 1),
    1: (2, 1, 0),
    2: (1, 0, 2),
}

Point = namedtuple('Point', ['x', 'y', 'z'])


class Piece:
    """
    Creates an object that represents a cube piece (edge, corner or center)
    """
    colors = {
        Color.WHITE: "white",
        Color.ORANGE: "orange",
        Color.GREEN: "green",
        Color.RED: "red",
        Color.BLUE: "blue",
        Color.YELLOW: "yellow",
    }

    def __init__(self, color_x, color_y, color_z):
        self.color = (color_x, color_y, color_z)

    def __str__(self):
        color_list = [self.colors.get(color) if color is not None else "None" for color in self.color]
        colors = "Colors:  X:" + color_list[0] + "  Y:" + color_list[1] + "  Z:" + color_list[2]
        return colors

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.color)

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return NotImplemented
        return self.color == other.color

    # Returns the type of the piece (1 = Center, 2 = Edge, 3 = Corner)
    def get_type(self):
        return sum(color is not None for color in self.color)

    # if a Piece is rotated around an axis, the colors of the other two axis have to be swapped
    def swap_colors(self, axis):
        swap = color_swaps[axis]
        self.color = (self.color[swap[0]], self.color[swap[1]], self.color[swap[2]])

    def get_rotation(self, pos):
        """
        returns the rotation of each piece that can be decided with some if-queries
        """
        if self.get_type() == 2:
            if pos.y != 1:
                if self.color[1] == Color['RED'] or self.color[1] == Color['ORANGE']:
                    return 1
                elif self.color[1] == Color['GREEN'] or self.color[1] == Color['BLUE']:
                    if Color['WHITE'] in self.color or Color['YELLOW'] in self.color:
                        return 1
                return 0
            else:
                if self.color[2] == Color['RED'] or self.color[2] == Color['ORANGE']:
                    return 1
                elif self.color[2] == Color['GREEN'] or self.color[2] == Color['BLUE']:
                    if Color['WHITE'] in self.color or Color['YELLOW'] in self.color:
                        return 1
                return 0

        elif self.get_type() == 3:
            if self.color[1] == Color['WHITE'] or self.color[1] == Color['YELLOW']:
                return 0
            elif self.color[0] == Color['WHITE'] or self.color[0] == Color['YELLOW']:
                if sum(coord for coord in pos) == 2 or sum(coord for coord in pos) == 6:
                    return 1
                else:
                    return 2
            else:
                if sum(coord for coord in pos) == 2 or sum(coord for coord in pos) == 6:
                    return 2
                else:
                    return 1

        else:
            return 0


class Cube:
    """
    Creates an object that represents a Rubik's Cube
    """
    def __init__(self, state=None):
        if state is None:
            state = cube_state

        # 3-dimensional Tuple to represent the cube
        self.pieces = (((Piece(state[1][6], state[5][6], state[4][8]), Piece(state[1][7], state[5][3], None), Piece(state[1][8], state[5][0], state[2][6])),
                        (Piece(state[1][3], None, state[4][5]), Piece(state[1][4], None, None), Piece(state[1][5], None, state[2][3])),
                        (Piece(state[1][0], state[0][0], state[4][2]), Piece(state[1][1], state[0][3], None), Piece(state[1][2], state[0][6], state[2][0]))
                        ),
                       ((Piece(None, state[5][7], state[4][7]), Piece(None, state[5][4], None), Piece(None, state[5][1], state[2][7])),
                        (Piece(None, None, state[4][4]), Piece(None, None, None), Piece(None, None, state[2][4])),
                        (Piece(None, state[0][1], state[4][1]), Piece(None, state[0][4], None), Piece(None, state[0][7], state[2][1]))
                        ),
                       ((Piece(state[3][8], state[5][8], state[4][6]), Piece(state[3][7], state[5][5], None), Piece(state[3][6], state[5][2], state[2][8])),
                        (Piece(state[3][5], None, state[4][3]), Piece(state[3][4], None, None), Piece(state[3][3], None, state[2][5])),
                        (Piece(state[3][2], state[0][2], state[4][0]), Piece(state[3][1], state[0][5], None), Piece(state[3][0], state[0][8], state[2][2]))
                        )
                       )

        self.faces = self.get_faces()

    def __hash__(self):
        return hash(self.pieces)

    def __eq__(self, other):
        if not isinstance(other, Cube):
            return NotImplemented
        return self.pieces == other.pieces

    def __str__(self):
        for piece in self.pieces:
            print(piece)
        return

    def __copy__(self):
        state = self.pieces_to_cube_state()
        return Cube(state)

    def pieces_to_cube_state(self):
        """
        converts the piece representation of a cube into a cubestate list
        """
        state = [None] * 6
        for face, pieces in self.faces.items():
            colors = [None] * 9
            axis = self.get_face_axis(face)
            for i, p in enumerate(pieces):
                pos = face_to_cubestate[face][i]
                colors[pos] = p.color[axis]
            assert all(color is not None for color in colors)
            state[colors[4].value] = colors
        return state

    def get_face_axis(self, face):
        if face == "R":
            return 0
        elif face == "L":
            return 0
        elif face == "U":
            return 1
        elif face == "D":
            return 1
        elif face == "F":
            return 2
        elif face == "B":
            return 2

    def get_edges(self):
        edges = [self.pieces[x][y][z]
                 for x in range(3)
                 for y in range(3)
                 for z in range(3)
                 if sum(color is None for color in self.pieces[x][y][z].color) == 1]
        return edges

    def get_corners(self):
        corners = [self.pieces[x][y][z]
                   for x in range(3)
                   for y in range(3)
                   for z in range(3)
                   if None not in self.pieces[x][y][z].color]
        return corners

    def get_faces(self):
        faces = {"R": [], "L": [], "U": [], "D": [], "F": [], "B": []}
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    if x == 0:
                        faces["L"].append(self.pieces[x][y][z])
                    elif x == 2:
                        faces["R"].append(self.pieces[x][y][z])
                    if y == 0:
                        faces["D"].append(self.pieces[x][y][z])
                    elif y == 2:
                        faces["U"].append(self.pieces[x][y][z])
                    if z == 0:
                        faces["B"].append(self.pieces[x][y][z])
                    elif z == 2:
                        faces["F"].append(self.pieces[x][y][z])
        return faces

    def rotate(self, face, direction):
        """
        applies a rotation to a cube by generating a new Tuple while swapping the appropriate Pieces
        """
        if direction == 'cw':
            rot = rotations[face]
        else:
            rot = inverse_rotations[face]
        self.pieces = tuple(
                        tuple(
                            tuple(
                                self.pieces[x][y][z] if (x, y, z) not in rot else self.pieces[rot[(x, y, z)][0]][rot[(x, y, z)][1]][rot[(x, y, z)][2]]
                                for z in range(3))
                            for y in range(3))
                        for x in range(3))

        self.faces = self.get_faces()

        for piece in self.faces[face]:
            piece.swap_colors(self.get_face_axis(face))

    def get_rotation_sum(self):
        edges = sum(self.pieces[x][y][z].get_rotation(Point(x, y, z))
                    for x in range(3)
                    for y in range(3)
                    for z in range(3)
                    if None in self.pieces[x][y][z].color)
        corners = sum(self.pieces[x][y][z].get_rotation(Point(x, y, z))
                      for x in range(3)
                      for y in range(3)
                      for z in range(3)
                      if None not in self.pieces[x][y][z].color)
        return edges, corners
