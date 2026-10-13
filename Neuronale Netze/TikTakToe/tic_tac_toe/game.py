"""Rules of tic-tac-toe, without any neural network.

A board is a list of 9 numbers, read row by row:

    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8

Each cell holds PLAYER_X (1), PLAYER_O (-1) or EMPTY (0). Using +1 / -1 means the other
player is always `-player`, and a board can be turned into "my view" by multiplying it.
"""

PLAYER_X = 1
PLAYER_O = -1
EMPTY = 0
CELL_COUNT = 9

# All 8 ways to get three in a row: 3 rows, 3 columns, 2 diagonals.
WIN_LINES: tuple[tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

SYMBOLS = {PLAYER_X: "X", PLAYER_O: "O", EMPTY: " "}


def new_board() -> list[int]:
    """Return an empty board."""
    return [EMPTY] * CELL_COUNT


def find_winner(board: list[int]) -> int:
    """Return PLAYER_X or PLAYER_O if one of them has three in a row, otherwise EMPTY."""
    for first, second, third in WIN_LINES:
        if board[first] != EMPTY and board[first] == board[second] == board[third]:
            return board[first]
    return EMPTY


def legal_moves(board: list[int]) -> list[int]:
    """Return the indices of all empty cells."""
    return [cell for cell in range(CELL_COUNT) if board[cell] == EMPTY]


def is_game_over(board: list[int]) -> bool:
    """The game ends when somebody has won or the board is full."""
    return find_winner(board) != EMPTY or not legal_moves(board)


def apply_move(board: list[int], cell: int, player: int) -> list[int]:
    """Return a copy of the board with the player's mark placed on the cell."""
    if not 0 <= cell < CELL_COUNT:
        raise ValueError(f"cell must be between 0 and 8, got {cell}")
    if board[cell] != EMPTY:
        raise ValueError(f"cell {cell} is already taken")
    next_board = list(board)
    next_board[cell] = player
    return next_board


def format_board(board: list[int]) -> str:
    """Draw the board as text; empty cells show their number so a player can pick one."""
    cells = [SYMBOLS[value] if value != EMPTY else str(cell) for cell, value in enumerate(board)]
    rows = [" | ".join(cells[start : start + 3]) for start in (0, 3, 6)]
    return "\n---------\n".join(rows)
