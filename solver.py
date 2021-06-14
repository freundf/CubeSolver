from copy import deepcopy
from queue import Queue
from constants import Faces
from cube_test import Cube
from pieces import pieces_solved

solved_cube = Cube()

def solve(state):
    cube = Cube(state)
    visited = {cube}
    queue = Queue()
    queue.put((cube, []))

    while not queue.empty():
        cube, path = queue.get()

        for face in Faces:
            for direction in ["cw", "ccw"]:
                new_cube = deepcopy(cube)
                new_cube.rotate(face.value, direction)

                if is_solved(new_cube):
                    solve_path = path + [(face, direction)]
                    print(solve_path)
                    return
                if new_cube not in visited:
                    queue.put((new_cube, path + [(face, direction)]))
                    visited.add(new_cube)


def is_solved(cube):
    if solved_cube.faces["U"] == cube.faces["U"]:
        return True
    else:
        return False


def state_tuple(state):
    return tuple(tuple(i) for i in state)





