from constants import Color, rotations, inverse_rotations, face_to_cubestate



"""
              +---------+
              | 0  1  2 |
              | 3 [0] 4 |
              | 5  6  7 |
    +---------+---------+---------+---------+
    | 0  1  2 | 0  1  2 | 0  1  2 | 0  1  2 |
    | 3 [1] 4 | 3 [2] 4 | 3 [3] 4 | 3 [4] 4 |
    | 5  6  7 | 5  6  7 | 5  6  7 | 5  6  7 |
    +---------+---------+---------+---------+
              | 0  1  2 |
              | 3 [5] 4 |
              | 5  6  7 |
              +---------+
"""
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


class Piece:
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
        self.rotation = 0

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

    def swap_colors(self, axis):
        swap = color_swaps[axis]
        self.color = (self.color[swap[0]], self.color[swap[1]], self.color[swap[2]])

    def get_rotation(self):  # TODO
        piece_type = sum(x is None for x in self.color)
        if piece_type == 0:     # Corner
            return 0

        elif piece_type == 1:   # Edge
            if self.color[0] == Color.WHITE or self.color[0] == Color.YELLOW:
                return 1
            else:
                if self.color[1] == Color.RED or self.color[1] == Color.ORANGE:
                    return 1
                else:
                    return 0

        elif piece_type >= 2:   # Center
            return 0


class Cube:

    def __init__(self, state=None):
        if state is None:
            state = [[color] * 9 for color in Color]

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
        rot_sum = 0
        for p in self.pieces:
            rot = p.get_rotation()
            rot_sum += rot
        return rot_sum


if __name__ == "__main__":
    c = Cube()
    c.rotate("R", 0)
