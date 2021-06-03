from tkinter import *
import numpy as np
from enum import Enum


class Color(Enum):
    WHITE = 0
    ORANGE = 1
    GREEN = 2
    RED = 3
    BLUE = 4
    YELLOW = 5


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

cube_state = [[color] * 9 for color in Color]
"""
              +---------+
              | 0  1  2 |
              | 3 [0] 4 |
              | 5  6  7 |
    +---------+---------+---------+---------+
    | 0  1  2 | 0  1  2 | 0  1  2 | 0  1  2 |
    | 3 [2] 4 | 3 [1] 4 | 3 [4] 4 | 3 [3] 4 |
    | 5  6  7 | 5  6  7 | 5  6  7 | 5  6  7 |
    +---------+---------+---------+---------+
              | 0  1  2 |
              | 3 [5] 4 |
              | 5  6  7 |
              +---------+
"""


class Piece:
    colors = {
        Color.WHITE: "white",
        Color.ORANGE: "orange",
        Color.GREEN: "green",
        Color.RED: "red",
        Color.BLUE: "blue",
        Color.YELLOW: "yellow",
    }

    def __init__(self, pos: list, color: list):
        self.pos = pos  # pos ist eine Liste mit Koordinaten (x, y, z)
        self.color = color

    def print_piece(self):
        print("Position:", self.pos)
        print("Colors:", "X:", self.color[0], "Y:", self.color[1], "Z:", self.color[2])

    def rotate(self, matrix):
        pos_mat = np.array([[self.pos[0]], [self.pos[1]], [self.pos[2]]])
        pos_mat = np.matmul(matrix, pos_mat)

        self.pos[0], self.pos[1], self.pos[2] = pos_mat[0][0], pos_mat[1][0], pos_mat[2][0]
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
            state = cube_state

        self.pieces = (Piece([-1, 1, -1], [cube_lst[18], cube_lst[0], cube_lst[29]]),
                       Piece([0, 1, -1], [None, cube_lst[1], cube_lst[28]]),
                       Piece([1, 1, -1], [cube_lst[38], cube_lst[2], cube_lst[27]]),
                       Piece([-1, 1, 0], [cube_lst[21], cube_lst[3], None]),
                       Piece([0, 1, 0], [None, cube_lst[4], None]),
                       Piece([1, 1, 0], [cube_lst[39], cube_lst[5], None]),
                       Piece([-1, 1, 1], [cube_lst[20], cube_lst[6], cube_lst[9]]),
                       Piece([0, 1, 1], [None, cube_lst[7], cube_lst[10]]),
                       Piece([1, 1, 1], [cube_lst[36], cube_lst[8], cube_lst[11]]),

                       Piece([-1, 0, -1], [cube_lst[21], None, cube_lst[32]]),
                       Piece([0, 0, -1], [None, None, cube_lst[31]]),
                       Piece([1, 0, -1], [cube_lst[41], None, cube_lst[30]]),
                       Piece([-1, 0, 0], [cube_lst[22], None, None]),
                       Piece([0, 0, 0], [None, None, None]),
                       Piece([1, 0, 0], [cube_lst[40], None, None]),
                       Piece([-1, 0, 1], [cube_lst[23], None, cube_lst[12]]),
                       Piece([0, 0, 1], [None, None, cube_lst[13]]),
                       Piece([1, 0, 1], [cube_lst[39], None, cube_lst[14]]),

                       Piece([-1, -1, -1], [cube_lst[24], cube_lst[51], cube_lst[35]]),
                       Piece([0, -1, -1], [None, cube_lst[52], cube_lst[34]]),
                       Piece([1, -1, -1], [cube_lst[44], cube_lst[53], cube_lst[33]]),
                       Piece([-1, -1, 0], [cube_lst[25], cube_lst[48], None]),
                       Piece([0, -1, 0], [None, cube_lst[49], None]),
                       Piece([1, -1, 0], [cube_lst[43], cube_lst[50], None]),
                       Piece([-1, -1, 1], [cube_lst[26], cube_lst[45], cube_lst[15]]),
                       Piece([0, -1, 1], [None, cube_lst[46], cube_lst[16]]),
                       Piece([1, -1, 1], [cube_lst[42], cube_lst[47], cube_lst[17]]))

        self.faces = self.get_faces()

    def get_faces(self):
        faces = {"R": {"Pieces": [piece for piece in self.pieces if piece.pos[0] == 1], "cw": rot_yz_cw, "ccw": rot_yz_ccw},
                 "L": {"Pieces": [piece for piece in self.pieces if piece.pos[0] == -1], "cw": rot_yz_ccw, "ccw": rot_yz_cw},
                 "U": {"Pieces": [piece for piece in self.pieces if piece.pos[1] == 1], "cw": rot_xz_cw, "ccw": rot_xz_ccw},
                 "D": {"Pieces": [piece for piece in self.pieces if piece.pos[1] == -1], "cw": rot_xz_ccw, "ccw": rot_xz_cw},
                 "F": {"Pieces": [piece for piece in self.pieces if piece.pos[2] == 1], "cw": rot_xy_cw, "ccw": rot_xy_ccw},
                 "B": {"Pieces": [piece for piece in self.pieces if piece.pos[2] == -1], "cw": rot_xy_ccw, "ccw": rot_xy_cw}
                 }
        return faces

    def print_cube(self):
        for p in self.pieces:
            p.print_piece()

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


class App:
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
    print(c.get_rotation_sum())
    a = App(c)
