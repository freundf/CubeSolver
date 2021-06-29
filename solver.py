from copy import copy
from queue import Queue
from time import time
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

# Create a cube with no rotations
solved_cube = Cube()


def solve(state):
    """
    Tries to find a solution with Breath-first-search
    """
    cube = Cube(state)
    if is_solved(cube):
        return ""
    visited = {cube}
    queue = Queue()
    queue.put((cube, []))

    time_start = time()
    time_cur = time_start

    # while-loop runs for 1 second
    while (time_cur - time_start) < 1:
        cube, path = queue.get()

        for face in Faces:
            for direction in ["cw", "ccw"]:
                new_cube = copy(cube)
                new_cube.rotate(face.value, direction)
                if is_solved(new_cube):
                    solve_path = path + [(face, direction)]
                    return path_to_string(solve_path)
                if new_cube not in visited:
                    queue.put((new_cube, path + [(face, direction)]))
                    visited.add(new_cube)
        time_cur = time()

    return solve_advanced(state)


def is_solved(cube):
    if solved_cube == cube:
        return True
    else:
        return False


def solve_advanced(state):
    """
    Solves the cube with kociemba's Algorithm
    """
    cube_string = cubestate_to_cubestring(state)
    path = kociemba_solve(cube_string, 20, 2)
    path = path.replace("3", "'").replace("1", "")
    path_list = path.split(" ")
    path_list.pop()
    path = " ".join(path_list)
    return path


def cubestate_to_cubestring(state):
    """
    Converts a cubestate to a string in the right format for kociemba's Algorithm
    """
    state = [state[0], state[3], state[2], state[5], state[1], state[4]]
    string = ""
    for face in state:
        for color in face:
            string += color_to_face[color.name]
    return string


def path_to_string(path):
    """
    Converts a found solution into a string
    """
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
    """
    Checks if a cube is solvable
    """
    cube = Cube(state)

    # Check if the cube contains the right pieces
    # Convert all piece colors to frozenset, so that rotations won't matter
    cube_set = set()
    solved_set = set()
    for x in range(3):
        for y in range(3):
            for z in range(3):
                # frozenset is required because it is hashable
                cube_set.add(frozenset(cube.pieces[x][y][z].color))
                solved_set.add(frozenset(solved_cube.pieces[x][y][z].color))
    if cube_set != solved_set:
        return False

    # Check the cube for permutation parity
    corner_perm = get_corner_permutation(cube)
    edge_perm = get_edge_permutation(cube)
    # A cube is solvable if the corner-permutation has the same parity as the edge-permutation
    if permutation_is_even(corner_perm) != permutation_is_even(edge_perm):
        return False

    # Check for orientation parity
    rotations = cube.get_rotation_sum()
    if rotations[0] % 2 != 0 or rotations[1] % 3 != 0:
        return False

    return True


def get_corner_permutation(cube):
    corners = cube.get_corners()
    solved = solved_cube.get_corners()
    cycles = get_cycles(corners, solved)
    return cycles


def get_edge_permutation(cube):
    edges = cube.get_edges()
    solved = solved_cube.get_edges()
    cycles = get_cycles(edges, solved)
    return cycles


def get_cycles(pieces, solved):
    for i in range(len(pieces)):
        pieces[i] = frozenset(pieces[i].color)
    for i in range(len(solved)):
        solved[i] = frozenset(solved[i].color)

    cycles = [[]]
    visited = []
    i = 0
    next_index = 0

    while set(visited) != set(pieces):
        if pieces[i] not in visited:
            visited.append(pieces[i])
            for j, solved_piece in enumerate(solved):
                if pieces[i] == solved_piece:
                    if i not in cycles[-1]:
                        cycles[-1].append(i)
                    next_index = j
            i = next_index
        else:
            cycles.append([])
            not_visited = [piece for piece in pieces if piece not in visited]
            if len(not_visited) != 0:
                i = pieces.index(not_visited[0])
    return cycles


def permutation_is_even(cycles):
    # a permutation is even if the number of cycles with even length is even
    even_cycles = [cyc for cyc in cycles if len(cyc) % 2 == 0]
    if len(even_cycles) % 2 == 0:
        return True
    else:
        return False
