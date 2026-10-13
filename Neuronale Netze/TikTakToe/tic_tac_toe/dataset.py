"""Training data: every position that can occur in a game, with its perfect moves.

Input  (9 numbers): the board seen from the player to move: 1 = my mark, -1 = opponent's
                    mark, 0 = empty. So the network never needs to know if it is X or O.
Target (9 numbers): 1 for every cell that minimax calls a best move, 0 for all others.
"""

import numpy as np

from tic_tac_toe.game import PLAYER_X, apply_move, is_game_over, legal_moves, new_board
from tic_tac_toe.minimax import best_moves


def encode_board(board: list[int], player: int) -> list[int]:
    """Turn the board into the network input: own marks become 1, the opponent's -1."""
    return [cell * player for cell in board]


def collect_positions() -> list[tuple[list[int], int]]:
    """Return every unfinished position reachable from the empty board, with the player to move."""
    seen: set[tuple[int, ...]] = set()
    positions: list[tuple[list[int], int]] = []
    # Positions still to visit. X always starts, so the board alone fixes whose turn it is.
    open_positions = [(new_board(), PLAYER_X)]

    while open_positions:
        board, player = open_positions.pop()
        if tuple(board) in seen or is_game_over(board):
            continue
        seen.add(tuple(board))
        positions.append((board, player))
        for cell in legal_moves(board):
            open_positions.append((apply_move(board, cell, player), -player))

    # Sorted so the data set has the same order on every run (reproducible training).
    positions.sort(key=lambda position: position[0])
    return positions


def load_dataset() -> tuple[np.ndarray, np.ndarray]:
    """Return inputs and targets as two float matrices with one row per position."""
    inputs = []
    targets = []
    for board, player in collect_positions():
        target = [0] * len(board)
        for cell in best_moves(board, player):
            target[cell] = 1
        inputs.append(encode_board(board, player))
        targets.append(target)
    return np.array(inputs, dtype=float), np.array(targets, dtype=float)
