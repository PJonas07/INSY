"""Let the network choose moves and measure how well it plays."""

from dataclasses import dataclass

import numpy as np

from tic_tac_toe.dataset import encode_board
from tic_tac_toe.game import (
    EMPTY,
    PLAYER_X,
    apply_move,
    find_winner,
    is_game_over,
    legal_moves,
    new_board,
)
from tic_tac_toe.network import NeuralNetwork

# Lower than any sigmoid output, so an occupied cell can never be chosen.
OCCUPIED_SCORE = -1.0


def choose_move(network: NeuralNetwork, board: list[int], player: int) -> int:
    """Return the empty cell whose output neuron is most active."""
    moves = legal_moves(board)
    if not moves:
        raise ValueError("the board is full, there is no move to choose")
    inputs = np.array(encode_board(board, player), dtype=float)
    outputs = network.forward(inputs).output_activations
    return max(moves, key=lambda cell: outputs[cell])


def best_move_rate(network: NeuralNetwork, inputs: np.ndarray, targets: np.ndarray) -> float:
    """Return the share of positions (0..1) in which the network picks one of the best moves."""
    outputs = network.forward(inputs).output_activations
    # A cell is empty exactly where the input is 0; occupied cells must not win the argmax.
    scores = np.where(inputs == EMPTY, outputs, OCCUPIED_SCORE)
    chosen_cells = np.argmax(scores, axis=1)
    is_best_move = targets[np.arange(len(inputs)), chosen_cells]
    return float(is_best_move.mean())


@dataclass
class Outcomes:
    """How many of the possible games the network wins, draws and loses."""

    wins: int = 0
    draws: int = 0
    losses: int = 0


def count_outcomes(network: NeuralNetwork, network_player: int) -> Outcomes:
    """Play the network against every possible sequence of opponent moves and count the results."""
    outcomes = Outcomes()

    def play_on(board: list[int], player: int) -> None:
        if is_game_over(board):
            winner = find_winner(board)
            if winner == network_player:
                outcomes.wins += 1
            elif winner == EMPTY:
                outcomes.draws += 1
            else:
                outcomes.losses += 1
            return
        if player == network_player:
            cell = choose_move(network, board, player)
            play_on(apply_move(board, cell, player), -player)
            return
        # The opponent tries every move, so no way to beat the network stays hidden.
        for cell in legal_moves(board):
            play_on(apply_move(board, cell, player), -player)

    play_on(new_board(), PLAYER_X)
    return outcomes
