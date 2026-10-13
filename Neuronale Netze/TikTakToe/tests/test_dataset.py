import numpy as np

from tic_tac_toe.dataset import collect_positions, encode_board, load_dataset
from tic_tac_toe.game import EMPTY, PLAYER_O, PLAYER_X, is_game_over, new_board

X, O, _ = PLAYER_X, PLAYER_O, EMPTY
# Known number of unfinished tic-tac-toe positions reachable when X starts.
POSITION_COUNT = 4520


def test_encode_board_keeps_the_view_of_x():
    board = [X, O, _, _, _, _, _, _, _]

    assert encode_board(board, X) == [1, -1, 0, 0, 0, 0, 0, 0, 0]


def test_encode_board_flips_the_view_for_o():
    board = [X, O, _, _, _, _, _, _, _]

    assert encode_board(board, O) == [-1, 1, 0, 0, 0, 0, 0, 0, 0]


def test_all_reachable_positions_are_collected_once():
    positions = collect_positions()

    boards = {tuple(board) for board, _player in positions}
    assert len(positions) == POSITION_COUNT
    assert len(boards) == POSITION_COUNT


def test_no_finished_game_is_in_the_data():
    assert not any(is_game_over(board) for board, _player in collect_positions())


def test_player_to_move_matches_the_number_of_marks():
    for board, player in collect_positions():
        is_x_turn = board.count(X) == board.count(O)

        assert player == (X if is_x_turn else O)


def test_empty_board_is_part_of_the_data():
    assert (new_board(), X) in collect_positions()


def test_dataset_shapes():
    inputs, targets = load_dataset()

    assert inputs.shape == (POSITION_COUNT, 9)
    assert targets.shape == (POSITION_COUNT, 9)


def test_every_position_has_at_least_one_best_move():
    _inputs, targets = load_dataset()

    assert np.all(targets.sum(axis=1) >= 1)


def test_best_moves_are_always_on_empty_cells():
    inputs, targets = load_dataset()

    assert np.all(inputs[targets == 1] == EMPTY)
