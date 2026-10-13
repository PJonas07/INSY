import numpy as np
import pytest

from tic_tac_toe.evaluation import Outcomes, best_move_rate, choose_move, count_outcomes
from tic_tac_toe.game import EMPTY, PLAYER_O, PLAYER_X
from tic_tac_toe.network import NeuralNetwork

X, O, _ = PLAYER_X, PLAYER_O, EMPTY
STRONG_BIAS = 10.0


def network_preferring(cell: int) -> NeuralNetwork:
    """Build a network that ignores the board and always rates one cell highest."""
    network = NeuralNetwork()
    network.weights_output[:] = 0.0
    network.bias_output[:] = 0.0
    network.bias_output[cell] = STRONG_BIAS
    return network


def test_choose_move_picks_the_most_active_output():
    network = network_preferring(6)

    assert choose_move(network, [_] * 9, X) == 6


def test_choose_move_never_picks_an_occupied_cell():
    network = network_preferring(4)
    board = [_, _, _, _, O, _, _, _, _]

    assert choose_move(network, board, X) != 4


def test_choose_move_on_full_board_raises():
    board = [X, O, X, X, O, O, O, X, X]

    with pytest.raises(ValueError):
        choose_move(NeuralNetwork(), board, X)


def test_best_move_rate_counts_matching_positions():
    network = network_preferring(0)
    inputs = np.zeros((2, 9))
    targets = np.zeros((2, 9))
    targets[0, 0] = 1  # first position: cell 0 is a best move, second position: it is not
    targets[1, 5] = 1

    assert best_move_rate(network, inputs, targets) == 0.5


def test_best_move_rate_ignores_occupied_cells():
    network = network_preferring(0)
    inputs = np.zeros((1, 9))
    inputs[0, 0] = -1  # the preferred cell is taken
    targets = np.zeros((1, 9))
    targets[0, 0] = 1

    assert best_move_rate(network, inputs, targets) == 0.0


def test_count_outcomes_covers_every_opponent_reply():
    outcomes = count_outcomes(network_preferring(4), X)

    game_count = outcomes.wins + outcomes.draws + outcomes.losses
    assert isinstance(outcomes, Outcomes)
    assert game_count > 0
    # A network that ignores the board must be beatable.
    assert outcomes.losses > 0
