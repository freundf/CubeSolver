from tkinter import *
import math
from collections import namedtuple
from cube import Cube
from constants import Color, Faces, moves
from solver import solve, solvable, solve_advanced
import random

Rectangle = namedtuple('Rectangle', ['start', 'end'])
Point = namedtuple('Point', ['x', 'y'])


class App:
    colors = {
        Color.WHITE: "white",
        Color.ORANGE: "orange",
        Color.GREEN: "green",
        Color.RED: "red",
        Color.BLUE: "blue",
        Color.YELLOW: "yellow",
    }

    margin = 5

    def __init__(self, state=None):
        if state is None:
            self.cube_state = self.state_reset()
        else:
            self.cube_state = state

        # Creates the root window
        self.root = Tk()
        self.root.geometry("500x700")
        self.root.configure(background="lightgray")

        # Creates the clickable cube display
        self.cube = Cube()
        self.cube_fr = Frame(self.root)
        self.cube_cv = Canvas(self.cube_fr, width=400, height=300)
        self.cube_cv.bind("<Button-1>", self.on_click)
        self.cube_cv.pack()

        # Creates the main menu
        self.menu = Frame(self.root, bg="lightgray")
        self.header = Label(self.menu, text="Cube Solver", font=("Helvetica", "50", "bold"),  bg="lightgray", pady=50)
        self.sim_btn = Button(self.menu, height=2, width=15, text="Simulation", font=("Helvetica", "20", "bold"), command=self.draw_simulation)
        self.slv_btn = Button(self.menu, height=2, width=15, text="Solver", font=("Helvetica", "20", "bold"), command=self.draw_solver)
        self.header.pack()
        self.slv_btn.pack()
        self.sim_btn.pack()

        # Creates the back and exit button
        self.menu_btn = Button(self.root, padx=30, pady=10, text="Back", command=self.draw_menu)
        self.exit_btn = Button(self.menu, height=2, width=15, text="Exit", font=("Helvetica", "15", "bold"), command=self.root.destroy)
        self.exit_btn.pack(side=BOTTOM, pady=150)

        # Creates the buttons to change color
        self.btn_cv = Canvas(self.root)
        self.color = None
        self.buttons = self.draw_buttons()

        # Creates the buttons to turn the cube
        self.moves_cv = Canvas(self.root)
        self.moves = self.draw_moves()

        # Create the random Scramble Button
        self.scramble_rnd = Button(self.root, text="Scramble", command=self.random_scramble)

        # Creates the scramble input
        self.scramble_input = Text(self.root, height=1, width=20, fg="white", font=("Helvetica", "20", "bold"))
        self.scramble_btn = Button(self.root, text="Set Scramble", command=self.set_scramble)
        self.solve_btn = Button(self.root, text="Find a Solution!", command=self.solve)

        self.solve_moves = StringVar()
        self.solution = Label(self.root, width=30, height=5, wraplength=300, textvariable=self.solve_moves, pady=20, font=("Helvetica", "20", "bold"), fg="white")

        self.error = Label(self.cube_fr, text="Your cube is not solvable!", font=("Helvetica", "20", "bold"), fg="white")

        self.draw_menu()

    def run(self):
        self.root.mainloop()

    def draw_menu(self):
        self.forget_widgets()

        self.menu.pack()

    def draw_solver(self):
        self.forget_widgets()

        self.cube_state = self.state_reset()
        self.draw_cube()
        self.btn_cv.pack()
        self.scramble_input.pack()
        self.scramble_btn.pack()
        self.solve_btn.pack()
        self.menu_btn.pack(side=BOTTOM, fill=BOTH)

    def draw_simulation(self):
        self.forget_widgets()

        self.cube_state = self.state_reset()
        self.scramble_rnd.pack()
        self.draw_cube()
        self.moves_cv.pack()
        self.menu_btn.pack(anchor=SW)

    def draw_solution(self, solution):
        self.forget_widgets()

        self.solve_moves.set(solution)
        self.solution.pack()
        self.menu_btn.pack(anchor=SW)

    # Unload all loaded widgets
    def forget_widgets(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()
        self.error.pack_forget()

    def draw_buttons(self):
        buttons = []
        for c in Color:
            btn = Button(self.btn_cv, background=self.colors[c], command=lambda x=c: self.set_color(x))
            btn.grid(column=c.value, row=0)
            buttons.append(btn)
        return buttons

    def draw_moves(self):
        buttons = []
        for i, f in enumerate(Faces):
            btn = Button(self.moves_cv, width=10, text=f.value, command=lambda x=f.value: self.rotate(x, "cw"))
            btn.grid(column=1, row=i, sticky="w")

            btn2_name = f.value + "'"
            btn2 = Button(self.moves_cv, width=10, text=btn2_name, command=lambda x=f.value: self.rotate(x, "ccw"))
            btn2.grid(column=2, row=i, sticky="e")
        return buttons

    def rotate(self, face, direction):
        self.cube.rotate(face, direction)
        self.cube_state = self.cube.pieces_to_cube_state()
        self.draw_cube()

    def solve(self):
        if solvable(self.cube_state):
            solution = solve_advanced(self.cube_state)
            self.draw_solution(solution)
            self.error.pack_forget()
        else:
            self.error.pack_forget()
            self.error.pack()

    def set_scramble(self):
        self.state_reset()
        scramble = self.scramble_input.get(1.0, "end-1c")
        scramble = list(scramble.upper().replace(" ", ""))

        delete = []
        for i,  move in enumerate(scramble):
            if move == "2" and i != 0:
                scramble[i] = scramble[i - 1]
            if move == "'" and i != 0:
                scramble[i - 1] += "'"
                delete.append(i)
        for i, v in enumerate(delete):
            scramble.pop(v - i)

        if not all(move in moves for move in scramble):
            self.scramble_input.delete(1.0, "end")
            self.scramble_input.insert(1.0, "False Scramble")
            return
        scramble = [moves[move] for move in scramble]

        for face, direction in scramble:
            self.rotate(face, direction)

    def random_scramble(self):
        scramble = [random.choice(list(moves.values())) for _ in range(20)]
        for face, direction in scramble:
            self.rotate(face, direction)

    def set_color(self, color):
        self.color = color

    def on_click(self, event):
        result = self.transform_coords_to_piece(event.x, event.y)
        if result is None or result[1] == 4 or self.color is None:
            return
        face, piece = result
        self.cube_state[face][piece] = self.color
        self.draw_cube()

    def draw_cube(self):
        self.cube_fr.pack(pady=5, padx=5)

        assert len(self.cube_state) == 6
        for face in range(6):
            self.draw_face(self.cube_state[face], self.face_to_coords(face))

    def draw_face(self, face, rect):
        assert len(face) == 9
        for x in range(3):
            for y in range(3):
                self.draw_piece(face[x + (3 * y)], rect, x, y)

    def draw_piece(self, color, rect, x_piece, y_piece):
        face_width = rect.end.x - rect.start.x
        face_height = rect.end.y - rect.start.y
        piece_width = face_width / 3
        piece_height = face_height / 3
        real_piece_x = x_piece * piece_width + rect.start.x
        real_piece_y = y_piece * piece_height + rect.start.y

        self.cube_cv.create_rectangle(real_piece_x, real_piece_y, real_piece_x + piece_width, real_piece_y + piece_height, fill=self.colors[color])

    def transform_coords_to_piece(self, x_coord, y_coord):
        for i, face_coords in ((face_num, self.face_to_coords(face_num)) for face_num in range(6)):
            if face_coords.start.x <= x_coord < face_coords.end.x and face_coords.start.y <= y_coord < face_coords.end.y:
                face = i
                x = math.floor((x_coord - face_coords.start.x) * 3 / (face_coords.end.x - face_coords.start.x))
                y = math.floor((y_coord - face_coords.start.y) * 3 / (face_coords.end.y - face_coords.start.y))
                piece = x + (3 * y)
                return face, piece

        return None

    def face_to_coords(self, face):
        assert 0 <= face < 6
        if face == 0:
            return self.face_coords_to_coords(1, 0)
        elif face == 5:
            return self.face_coords_to_coords(1, 2)
        else:
            return self.face_coords_to_coords(face-1, 1)

    def face_coords_to_coords(self, x_face, y_face):
        width_without_margins = int(self.cube_cv["width"]) - 5 * self.margin
        height_without_margins = int(self.cube_cv["height"]) - 4 * self.margin
        face_width = width_without_margins / 4
        face_height = height_without_margins / 3
        scaled_face_x = x_face * face_width + (x_face + 1) * self.margin
        scaled_face_y = y_face * face_height + (y_face + 1) * self.margin

        start = Point(scaled_face_x, scaled_face_y)
        end = Point(scaled_face_x + face_width, scaled_face_y + face_height)

        return Rectangle(start, end)

    def state_reset(self):
        self.cube = Cube()
        return [[color] * 9 for color in Color]


if __name__ == "__main__":
    a = App()
    a.run()
