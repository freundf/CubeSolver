from copy import copy
from queue import Queue
from constants import Faces
from cube_test import Cube

solved_cube = Cube()


def solve(state):
    cube = Cube(state)
    if is_solved_f2l(cube):
        return []
    visited = {cube}
    queue = Queue()
    queue.put((cube, []))

    while not queue.empty():
        cube, path = queue.get()

        for face in Faces:
            for direction in ["cw", "ccw"]:
                new_cube = copy(cube)
                new_cube.rotate(face.value, direction)

                if is_solved_f2l(new_cube):
                    solve_path = path + [(face, direction)]
                    print(solve_path)
                    return path_to_string(solve_path)
                if new_cube not in visited:
                    queue.put((new_cube, path + [(face, direction)]))
                    visited.add(new_cube)


def is_solved_cross(cube):
    if solved_cube.faces["U"][1::2] == cube.faces["U"][1::2]:
        return True
    else:
        return False


def is_solved_f2l(cube):
    if solved_cube.faces["F"][0:2] == cube.faces["F"][0:2]:
        return True
    else:
        return False


def path_to_string(path):
    moves = [move[0].value if move[1] == "cw" else (move[0].value + "'") for move in path]
    delete = []
    for i, move in enumerate(moves[:-1]):
        if moves[i + 1] == move:
            moves[i] = move + "2"
            delete.append(i + 1)

    for i, v in enumerate(delete):
        moves.pop(v - i)

    string = ', '.join(moves)
    print(string)
    return string
