from copy import copy
from queue import Queue
from constants import Faces
from cube import Cube
from kociemba.solver import solve as kociemba_solve


color_to_face = {
    "WHITE": "U",
    "YELLOW": "D",
    "GREEN": "F",
    "BLUE": "B",
    "RED": "R",
    "ORANGE": "L",
}


def cubestate_to_cubestring(state):
    state = [state[0], state[3], state[2], state[5], state[1], state[4]]
    string = ""
    for face in state:
        for color in face:
            string += color_to_face[color.name]
    return string


def solve_advanced(state):
    cube_string = cubestate_to_cubestring(state)
    path = kociemba_solve(cube_string, 18, 2)
    path = path.replace("3", "'").replace("1", "")
    path_list = path.split(" ")
    path_list.pop()
    path = " ".join(path_list)
    return path


solved_cube = Cube()


def solve(state):
    cube = Cube(state)
    if is_solved_cross(cube):
        return ""
    visited = {cube}
    queue = Queue()
    queue.put((cube, []))

    while not queue.empty():
        cube, path = queue.get()

        for face in Faces:
            for direction in ["cw", "ccw"]:
                new_cube = copy(cube)
                new_cube.rotate(face.value, direction)
                if is_solved_cross(new_cube):
                    solve_path = path + [(face, direction)]
                    return path_to_string(solve_path)
                if new_cube not in visited:
                    queue.put((new_cube, path + [(face, direction)]))
                    visited.add(new_cube)


def is_solved_cross(cube):
    if solved_cube.faces["D"][1::2] == cube.faces["D"][1::2]:
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

    string = " ".join(moves)
    return string


def solvable(state):
    cube = Cube(state)

    # Convert all piece colors to frozenset, so that rotations won't matter
    cube_set = set()
    solved_set = set()
    for x in range(3):
        for y in range(3):
            for z in range(3):
                # frozenset is required because it is hashable
                cube_set.add(frozenset(cube.pieces[x][y][z].color))
                solved_set.add(frozenset(solved_cube.pieces[x][y][z].color))

    rotations = cube.get_rotation_sum()
    if cube_set == solved_set and rotations[0] % 2 == 0 and rotations[1] % 3 == 0:
        return True
    else:
        return False

