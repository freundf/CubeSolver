from sympy.combinatorics.permutations import Permutation

a = Permutation([[0, 1, 2, 3], [4, 5, 6]])
print(a.is_even)




"""
from copy import copy
from queue import Queue
from constants import Faces, Color
from cube import Cube

import profile

solved_cube = Cube()

def solve(state):
    cube = Cube(state)
    visited = {cube}
    queue = Queue()
    queue.put((cube, []))

    i = 0

    while i <= 100:
        cube, path = queue.get()

        for face in Faces:
            for direction in ["cw", "ccw"]:
                new_cube = copy(cube)
                new_cube.rotate(face.value, direction)

                if is_solved(new_cube):
                    solve_path = path + [(face, direction)]
                    print(solve_path)
                    return
                if new_cube not in visited:
                    queue.put((new_cube, path + [(face, direction)]))
                    visited.add(new_cube)
        i += 1


def is_solved(cube):
    if solved_cube.faces["U"] == cube.faces["U"]:
        return True
    else:
        return False


def state_tuple(state):
    return tuple(tuple(i) for i in state)

state = [[color] * 9 for color in Color]
state[0][3] = state[2][1]

profile.run("solve(state)")
"""
