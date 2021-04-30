from tkinter import *
import numpy as np

matrix_cw = np.array([[0, -1], [1, 0]])
matrix_ccw = np.array([[0, 1], [-1, 0]])


class Piece:
    def __init__(self, pos: list, color: str):
        self.pos = pos
        self.color = color

    def print_piece(self):
        print(self.pos, self.color)

    def rotate(self, dir):
        pos_mat = np.array([[self.pos[0]], [self.pos[1]]])
        if dir == "cw":
            pos_mat = np.matmul(matrix_cw, pos_mat)
        else:
            pos_mat = np.matmul(matrix_ccw, pos_mat)

        self.pos[0], self.pos[1] = pos_mat[0][0], pos_mat[1][0]


class Cube:
    def __init__(self):
        self.pieces = (Piece([-1, -1], "blue"),
                       Piece([-1, 0], "green"),
                       Piece([-1, 1], "yellow"),
                       Piece([0, -1], "red"),
                       Piece([0, 0], "white"),
                       Piece([0, 1], "red"),
                       Piece([1, -1], "green"),
                       Piece([1, 0], "orange"),
                       Piece([1, 1], "green"))

    def print_cube(self):
        for p in self.pieces:
            p.print_piece()

    def rotate(self, dir):
        for p in self.pieces:
            p.rotate(dir)


class App:
    def __init__(self):
        self.cube = Cube()

        self.root = Tk()
        self.root.configure(background="lightgray")
        self.cube_fr = Frame(self.root)
        self.cube_fr.pack(padx=5, pady=5)
        self.print(self.cube)

        self.btn_cw = Button(self.root, text="Rotate CW", width=50, command=self.rotate_cw)
        self.btn_ccw = Button(self.root, text="Rotate CCW", width=50, command=self.rotate_ccw)
        self.btn_cw.pack()
        self.btn_ccw.pack()
        self.root.mainloop()

    def rotate_cw(self):
        self.cube.rotate("cw")
        self.print(self.cube)

    def rotate_ccw(self):
        self.cube.rotate("ccw")
        self.print(self.cube)

    def print(self, cube):
        for p in cube.pieces:
            cv = Canvas(self.cube_fr, width=20, height=20, background=p.color, highlightthickness=1, highlightbackground="black")
            cv.grid(column=p.pos[0]+1, row=p.pos[1]+1)


a = App()
