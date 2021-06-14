from tkinter import *
import numpy as np


from constants import Color


rot_xy_cw = np.array([[0, 1, 0],
                      [-1, 0, 0],
                      [0, 0, 1]])

rot_xy_ccw = np.array([[0, -1, 0],
                       [1, 0, 0],
                       [0, 0, 1]])

rot_xz_cw = np.array([[0, 0, -1],
                      [0, 1, 0],
                      [1, 0, 0]])

rot_xz_ccw = np.array([[0, 0, 1],
                       [0, 1, 0],
                       [-1, 0, 0]])

rot_yz_cw = np.array([[1, 0, 0],
                      [0, 0, 1],
                      [0, -1, 0]])

rot_yz_ccw = np.array([[1, 0, 0],
                       [0, 0, -1],
                       [0, 1, 0]])


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


class Piece:
    colors = {
        Color.WHITE: "white",
        Color.ORANGE: "orange",
        Color.GREEN: "green",
        Color.RED: "red",
        Color.BLUE: "blue",
        Color.YELLOW: "yellow",
    }

    def __init__(self, pos, color):
        self.pos = pos  # pos ist ein Tupel mit Koordinaten (x, y, z)
        self.color = color
        self.rotation = 0

    def __str__(self):
        pos = "Position: "
        for i in self.pos:
            pos += str(i) + " "

        color_list = [self.colors.get(color) if color is not None else "None" for color in self.color]
        colors = "Colors:  X:" + color_list[0] + "  Y:" + color_list[1] + "  Z:" + color_list[2]
        return pos + "\n" + colors

    def __hash__(self):
        return hash(tuple(self.pos)) + hash(tuple(self.color)) + hash(self.rotation)

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return NotImplemented
        return self.pos == other.pos and self.color == other.color


    def rotate(self, matrix):
        pos_mat = np.array([[self.pos[0]], [self.pos[1]], [self.pos[2]]])
        pos_mat = np.matmul(matrix, pos_mat)

        self.pos = pos_mat[0][0], pos_mat[1][0], pos_mat[2][0]
        self.swap_colors(matrix)

    def swap_colors(self, matrix):
        swap = [i[0] for i, v in np.ndenumerate(np.diag(matrix)) if v != 1]
        self.color[swap[0]], self.color[swap[1]] = self.color[swap[1]], self.color[swap[0]]

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

        self.pieces = (Piece([-1, 1, -1], [state[1][0], state[0][0], state[4][2]]),
                       Piece([0, 1, -1], [None, state[0][1], state[4][1]]),
                       Piece([1, 1, -1], [state[3][2], state[0][2], state[4][0]]),
                       Piece([-1, 1, 0], [state[1][1], state[0][3], None]),
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
                       Piece([1, 0, 1], [state[3][5], None, state[2][5]]),

                       Piece([-1, -1, -1], [state[1][6], state[5][6], state[4][8]]),
                       Piece([0, -1, -1], [None, state[5][7], state[4][7]]),
                       Piece([1, -1, -1], [state[3][8], state[5][8], state[4][6]]),
                       Piece([-1, -1, 0], [state[1][7], state[5][3], None]),
                       Piece([0, -1, 0], [None, state[5][4], None]),
                       Piece([1, -1, 0], [state[3][7], state[5][5], None]),
                       Piece([-1, -1, 1], [state[1][8], state[5][0], state[2][6]]),
                       Piece([0, -1, 1], [None, state[5][1], state[2][7]]),
                       Piece([1, -1, 1], [state[3][6], state[5][2], state[2][8]]))

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

    def pieces_to_cube_state(self):
        state = [None] * 6
        for face, value in self.faces.items():
            colors = [None] * 9
            pieces = value.get("Pieces")
            axis = self.get_face_axis(face)
            for p in pieces:
                pos_in_face = tuple(x * y for x, y in zip(p.pos, face_axis[face]))
                real_pos = pos_in_face[face_encoding[face][0]] + 1 + 3 * (pos_in_face[face_encoding[face][1]] + 1)
                colors[real_pos] = p.color[axis]
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
        faces = {"R": {"Pieces": [piece for piece in self.pieces if piece.pos[0] == 1], "cw": rot_yz_cw, "ccw": rot_yz_ccw},
                 "L": {"Pieces": [piece for piece in self.pieces if piece.pos[0] == -1], "cw": rot_yz_ccw, "ccw": rot_yz_cw},
                 "U": {"Pieces": [piece for piece in self.pieces if piece.pos[1] == 1], "cw": rot_xz_cw, "ccw": rot_xz_ccw},
                 "D": {"Pieces": [piece for piece in self.pieces if piece.pos[1] == -1], "cw": rot_xz_ccw, "ccw": rot_xz_cw},
                 "F": {"Pieces": [piece for piece in self.pieces if piece.pos[2] == 1], "cw": rot_xy_cw, "ccw": rot_xy_ccw},
                 "B": {"Pieces": [piece for piece in self.pieces if piece.pos[2] == -1], "cw": rot_xy_ccw, "ccw": rot_xy_cw}
                 }
        return faces

    def rotate(self, face, dir):
        pieces = self.faces.get(face).get("Pieces")
        matrix = self.faces.get(face).get(dir)
        for p in pieces:
            p.rotate(matrix)
        self.faces = self.get_faces()

    def get_rotation_sum(self):
        rot_sum = 0
        for p in self.pieces:
            rot = p.get_rotation()
            rot_sum += rot
        return rot_sum


class AppTest:
    def __init__(self, cube):
        self.cube = cube

        self.root = Tk()
        self.root.configure(background="lightgray")
        self.cube_fr = Frame(self.root)
        self.cube_fr.pack(padx=5, pady=5)
        self.face_l = Frame(self.cube_fr, background="black")
        self.face_u = Frame(self.cube_fr, background="black")
        self.face_f = Frame(self.cube_fr, background="black")
        self.face_d = Frame(self.cube_fr, background="black")
        self.face_r = Frame(self.cube_fr, background="black")
        self.face_b = Frame(self.cube_fr, background="black")

        self.print_colors(self.cube)

        self.face_l.grid(column=0, row=1, padx=2, pady=2)
        self.face_u.grid(column=1, row=0, padx=2, pady=2)
        self.face_f.grid(column=1, row=1, padx=2, pady=2)
        self.face_d.grid(column=1, row=2, padx=2, pady=2)
        self.face_r.grid(column=2, row=1, padx=2, pady=2)
        self.face_b.grid(column=3, row=1, padx=2, pady=2)

        self.btn_r = Button(self.root, text="R", width=50, command=lambda: self.rotate("R", "cw"))
        self.btn_l = Button(self.root, text="L", width=50, command=lambda: self.rotate("L", "cw"))
        self.btn_u = Button(self.root, text="U", width=50, command=lambda: self.rotate("U", "cw"))
        self.btn_d = Button(self.root, text="D", width=50, command=lambda: self.rotate("D", "cw"))
        self.btn_f = Button(self.root, text="F", width=50, command=lambda: self.rotate("F", "cw"))
        self.btn_b = Button(self.root, text="B", width=50, command=lambda: self.rotate("B", "cw"))

        self.btn_r.pack()
        self.btn_l.pack()
        self.btn_u.pack()
        self.btn_d.pack()
        self.btn_f.pack()
        self.btn_b.pack()

        self.button = Button(self.root, command=c.pieces_to_cube_state)
        self.button.pack()

        self.root.mainloop()

    def rotate(self, face, dir):
        self.cube.rotate(face, dir)
        self.print_colors(self.cube)

    def print_colors(self, cube):
        for p in cube.pieces:
            if p.pos[0] == -1:  # left Face
                cv = Canvas(self.face_l, width=20, height=20, background=p.color[0].name, highlightthickness=1, highlightbackground="black")
                cv.grid(column=p.pos[2] + 1, row=1 - p.pos[1])
            if p.pos[0] == 1:   # right face
                cv = Canvas(self.face_r, width=20, height=20, background=p.color[0].name, highlightthickness=1, highlightbackground="black")
                cv.grid(column=1 - p.pos[2], row=1 - p.pos[1])
            if p.pos[1] == -1:  # down face
                cv = Canvas(self.face_d, width=20, height=20, background=p.color[1].name, highlightthickness=1, highlightbackground="black")
                cv.grid(column=p.pos[0] + 1, row=1 - p.pos[2])
            if p.pos[1] == 1:   # up face
                cv = Canvas(self.face_u, width=20, height=20, background=p.color[1].name, highlightthickness=1, highlightbackground="black")
                cv.grid(column=p.pos[0] + 1, row=p.pos[2] + 1)
            if p.pos[2] == -1:  # back face
                cv = Canvas(self.face_b, width=20, height=20, background=p.color[2].name, highlightthickness=1, highlightbackground="black")
                cv.grid(column=1 - p.pos[0], row=1 - p.pos[1])
            if p.pos[2] == 1:   # front face
                cv = Canvas(self.face_f, width=20, height=20, background=p.color[2].name, highlightthickness=1, highlightbackground="black")
                cv.grid(column=p.pos[0] + 1, row=1 - p.pos[1])


if __name__ == "__main__":
    c = Cube()
    a = AppTest(c)
