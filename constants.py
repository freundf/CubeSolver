from enum import Enum


class Color(Enum):
    WHITE = 0
    ORANGE = 1
    GREEN = 2
    RED = 3
    BLUE = 4
    YELLOW = 5


class Faces(Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"
    FRONT = "F"
    BACK = "B"


# maps piece coordinates to the new coordinates after a face rotation
rotations = {
    "R": {(2, 0, 2): (2, 0, 0),
          (2, 2, 2): (2, 0, 2),
          (2, 2, 0): (2, 2, 2),
          (2, 0, 0): (2, 2, 0),

          (2, 1, 2): (2, 0, 1),
          (2, 2, 1): (2, 1, 2),
          (2, 1, 0): (2, 2, 1),
          (2, 0, 1): (2, 1, 0)
          },

    "L": {(0, 2, 0): (0, 0, 0),
          (0, 2, 2): (0, 2, 0),
          (0, 0, 2): (0, 2, 2),
          (0, 0, 0): (0, 0, 2),

          (0, 1, 0): (0, 0, 1),
          (0, 2, 1): (0, 1, 0),
          (0, 1, 2): (0, 2, 1),
          (0, 0, 1): (0, 1, 2)
          },

    "U": {(2, 2, 0): (0, 2, 0),
          (2, 2, 2): (2, 2, 0),
          (0, 2, 2): (2, 2, 2),
          (0, 2, 0): (0, 2, 2),

          (2, 2, 1): (1, 2, 0),
          (1, 2, 2): (2, 2, 1),
          (0, 2, 1): (1, 2, 2),
          (1, 2, 0): (0, 2, 1)
          },

    "D": {(0, 0, 2): (0, 0, 0),
          (2, 0, 2): (0, 0, 2),
          (2, 0, 0): (2, 0, 2),
          (0, 0, 0): (2, 0, 0),

          (0, 0, 1): (1, 0, 0),
          (1, 0, 2): (0, 0, 1),
          (2, 0, 1): (1, 0, 2),
          (1, 0, 0): (2, 0, 1)
          },

    "F": {(2, 2, 2): (0, 2, 2),
          (2, 0, 2): (2, 2, 2),
          (0, 0, 2): (2, 0, 2),
          (0, 2, 2): (0, 0, 2),

          (1, 2, 2): (0, 1, 2),
          (2, 1, 2): (1, 2, 2),
          (1, 0, 2): (2, 1, 2),
          (0, 1, 2): (1, 0, 2)
          },

    "B": {(2, 0, 0): (0, 0, 0),
          (2, 2, 0): (2, 0, 0),
          (0, 2, 0): (2, 2, 0),
          (0, 0, 0): (0, 2, 0),

          (2, 1, 0): (1, 0, 0),
          (1, 2, 0): (2, 1, 0),
          (0, 1, 0): (1, 2, 0),
          (1, 0, 0): (0, 1, 0)
          }
}

inverse_rotations = {
    "R": {(2, 0, 0): (2, 0, 2),
          (2, 0, 2): (2, 2, 2),
          (2, 2, 2): (2, 2, 0),
          (2, 2, 0): (2, 0, 0),

          (2, 0, 1): (2, 1, 2),
          (2, 1, 2): (2, 2, 1),
          (2, 2, 1): (2, 1, 0),
          (2, 1, 0): (2, 0, 1)
          },

    "L": {(0, 0, 0): (0, 2, 0),
          (0, 2, 0): (0, 2, 2),
          (0, 2, 2): (0, 0, 2),
          (0, 0, 2): (0, 0, 0),

          (0, 0, 1): (0, 1, 0),
          (0, 1, 0): (0, 2, 1),
          (0, 2, 1): (0, 1, 2),
          (0, 1, 2): (0, 0, 1)
          },

    "U": {(0, 2, 0): (2, 2, 0),
          (2, 2, 0): (2, 2, 2),
          (2, 2, 2): (0, 2, 2),
          (0, 2, 2): (0, 2, 0),

          (1, 2, 0): (2, 2, 1),
          (2, 2, 1): (1, 2, 2),
          (1, 2, 2): (0, 2, 1),
          (0, 2, 1): (1, 2, 0)
          },

    "D": {(0, 0, 0): (0, 0, 2),
          (0, 0, 2): (2, 0, 2),
          (2, 0, 2): (2, 0, 0),
          (2, 0, 0): (0, 0, 0),

          (1, 0, 0): (0, 0, 1),
          (0, 0, 1): (1, 0, 2),
          (1, 0, 2): (2, 0, 1),
          (2, 0, 1): (1, 0, 0)
          },

    "F": {(0, 2, 2): (2, 2, 2),
          (2, 2, 2): (2, 0, 2),
          (2, 0, 2): (0, 0, 2),
          (0, 0, 2): (0, 2, 2),

          (0, 1, 2): (1, 2, 2),
          (1, 2, 2): (2, 1, 2),
          (2, 1, 2): (1, 0, 2),
          (1, 0, 2): (0, 1, 2)
          },

    "B": {(0, 0, 0): (2, 0, 0),
          (2, 0, 0): (2, 2, 0),
          (2, 2, 0): (0, 2, 0),
          (0, 2, 0): (0, 0, 0),

          (1, 0, 0): (2, 1, 0),
          (2, 1, 0): (1, 2, 0),
          (1, 2, 0): (0, 1, 0),
          (0, 1, 0): (1, 0, 0)
          }
}


# maps a face coordinate to the cubestate coordinate
face_to_cubestate = {
    "R": {0: 8,
          1: 7,
          2: 6,
          3: 5,
          4: 4,
          5: 3,
          6: 2,
          7: 1,
          8: 0
          },

    "L": {0: 6,
          1: 7,
          2: 8,
          3: 3,
          4: 4,
          5: 5,
          6: 0,
          7: 1,
          8: 2
          },

    "U": {0: 0,
          1: 3,
          2: 6,
          3: 1,
          4: 4,
          5: 7,
          6: 2,
          7: 5,
          8: 8
          },

    "D": {0: 6,
          1: 3,
          2: 0,
          3: 7,
          4: 4,
          5: 1,
          6: 8,
          7: 5,
          8: 2
          },

    "F": {0: 6,
          1: 3,
          2: 0,
          3: 7,
          4: 4,
          5: 1,
          6: 8,
          7: 5,
          8: 2
          },

    "B": {0: 8,
          1: 5,
          2: 2,
          3: 7,
          4: 4,
          5: 1,
          6: 6,
          7: 3,
          8: 0
          }
}

# maps a move-string to a move
moves = {
      "R": ("R", "cw"),
      "R'": ("R", "ccw"),
      "L": ("L", "cw"),
      "L'": ("L", "ccw"),
      "U": ("U", "cw"),
      "U'": ("U", "ccw"),
      "D": ("D", "cw"),
      "D'": ("D", "ccw"),
      "F": ("F", "cw"),
      "F'": ("F", "ccw"),
      "B": ("B", "cw"),
      "B'": ("B", "ccw"),
}
