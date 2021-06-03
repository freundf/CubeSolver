import math
from collections import namedtuple
from tkinter import Tk, Frame, Canvas, Button
from enum import Enum


class Color(Enum):
    WHITE = 0
    ORANGE = 1
    GREEN = 2
    RED = 3
    BLUE = 4
    YELLOW = 5


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

    def __init__(self):
        self.cube_state = [[color] * 9 for color in Color]
        self.root = Tk()
        self.root.configure(background="lightgray")
        self.cube_fr = Frame(self.root)
        self.cube_fr.pack(padx=5, pady=5)

        self.cube_cv = Canvas(self.cube_fr, width=400, height=300)
        self.cube_cv.pack()
        self.cube_cv.bind("<Button-1>", self.on_click)

        self.draw_cube()

        self.btn_cv = Canvas(self.root)
        self.color = Color.WHITE
        self.buttons = self.draw_buttons()
        self.btn_cv.pack()

        self.root.mainloop()

    def draw_buttons(self):
        buttons = []
        for c in Color:
            btn = Button(self.btn_cv, background=self.colors[c], command=lambda x=c: self.set_color(x))
            btn.grid(column=c.value, row=0)
            buttons.append(btn)
        return buttons

    def set_color(self, color):
        self.color = color

    def on_click(self, event):
        result = self.transform_coords_to_piece(event.x, event.y)
        if result is None or result[1] == 4:
            return
        face, piece = result
        self.cube_state[face][piece] = self.color
        self.draw_cube()

    def draw_cube(self):
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


if __name__ == "__main__":
    a = App()
