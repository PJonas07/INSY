import pytest

from tic_tac_toe.game import (
    EMPTY,
    PLAYER_O,
    PLAYER_X,
    WIN_LINES,
    apply_move,
    find_winner,
    format_board,
    is_game_over,
    legal_moves,
    new_board,
)

X, O, _ = PLAYER_X, PLAYER_O, EMPTY


def test_new_board_has_nine_empty_cells():
    assert new_board() == [EMPTY] * 9


@pytest.mark.parametrize("line", WIN_LINES)
def test_every_win_line_is_detected(line):
    board = new_board()
    for cell in line:
        board[cell] = O

    assert find_winner(board) == O


def test_no_winner_on_empty_board():
    assert find_winner(new_board()) == EMPTY


def test_two_in_a_row_is_not_a_win():
    board = [X, X, _, _, _, _, _, _, _]

    assert find_winner(board) == EMPTY


def test_legal_moves_are_the_empty_cells():
    board = [X, O, _, _, X, _, _, _, O]

    assert legal_moves(board) == [2, 3, 5, 6, 7]


def test_game_is_over_after_a_win():
    board = [X, X, X, O, O, _, _, _, _]

    assert is_game_over(board)


def test_game_is_over_when_board_is_full_without_winner():
    board = [X, O, X, X, O, O, O, X, X]

    assert find_winner(board) == EMPTY
    assert is_game_over(board)


def test_game_is_not_over_at_the_start():
    assert not is_game_over(new_board())


def test_apply_move_places_mark_and_keeps_original_board():
    board = new_board()

    next_board = apply_move(board, 4, X)

    assert next_board[4] == X
    assert board[4] == EMPTY


def test_apply_move_rejects_taken_cell():
    board = apply_move(new_board(), 4, X)

    with pytest.raises(ValueError):
        apply_move(board, 4, O)


@pytest.mark.parametrize("cell", [-1, 9])
def test_apply_move_rejects_cell_outside_board(cell):
    with pytest.raises(ValueError):
        apply_move(new_board(), cell, X)


def test_format_board_shows_marks_and_free_cell_numbers():
    board = [X, _, _, _, O, _, _, _, _]

    assert format_board(board) == "X | 1 | 2\n---------\n3 | O | 5\n---------\n6 | 7 | 8"
