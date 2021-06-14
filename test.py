from copy import deepcopy
from queue import Queue
from tkinter import *
from enum import Enum
import profile

from constants import Faces, Color
from cube import Cube
from solver import state_tuple, is_solved


def solve(state):
    visited = {state_tuple(state)}
    queue = Queue()
    queue.put((state, []))
    i = 0
    while i <= 10:
        state, path = queue.get()
        cube = Cube(state)
        if is_solved(cube):
            print(path)
            return
        for face in Faces:
            for direction in ["cw", "ccw"]:
                cube = Cube(deepcopy(state))
                cube.rotate(face.value, direction)
                new_state = cube.pieces_to_cube_state()
                new_state_tuple = (state_tuple(new_state))
                if new_state_tuple not in visited:
                    queue.put((new_state, path + [(face, direction)]))
                    visited.add(new_state_tuple)
        i += 1


state = [[color] * 9 for color in Color]
state[0], state[3] = state[3], state[0]

profile.run("solve(state)")
