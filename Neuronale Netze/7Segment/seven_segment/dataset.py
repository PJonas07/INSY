"""Training data: which segments light up for each digit.

Segment layout (standard naming):

     aaa
    f   b
    f   b
     ggg
    e   c
    e   c
     ddd
"""

import numpy as np

SEGMENT_NAMES = ("a", "b", "c", "d", "e", "f", "g")
DIGIT_COUNT = 10

# One row per digit, columns in the order a, b, c, d, e, f, g (1 = segment on).
SEGMENT_TABLE: tuple[tuple[int, ...], ...] = (
    (1, 1, 1, 1, 1, 1, 0),  # 0
    (0, 1, 1, 0, 0, 0, 0),  # 1
    (1, 1, 0, 1, 1, 0, 1),  # 2
    (1, 1, 1, 1, 0, 0, 1),  # 3
    (0, 1, 1, 0, 0, 1, 1),  # 4
    (1, 0, 1, 1, 0, 1, 1),  # 5
    (1, 0, 1, 1, 1, 1, 1),  # 6
    (1, 1, 1, 0, 0, 0, 0),  # 7
    (1, 1, 1, 1, 1, 1, 1),  # 8
    (1, 1, 1, 1, 0, 1, 1),  # 9
)


def load_inputs() -> np.ndarray:
    """Return the segment patterns as a (10, 7) float matrix, row i = digit i."""
    return np.array(SEGMENT_TABLE, dtype=float)


def load_targets() -> np.ndarray:
    """Return the expected outputs as a (10, 10) one-hot matrix (identity matrix)."""
    return np.eye(DIGIT_COUNT)


def segments_for_digit(digit: int) -> list[int]:
    """Return the 7 segment states for a digit, e.g. 1 -> [0, 1, 1, 0, 0, 0, 0]."""
    if not 0 <= digit < DIGIT_COUNT:
        raise ValueError(f"digit must be between 0 and 9, got {digit}")
    return list(SEGMENT_TABLE[digit])
