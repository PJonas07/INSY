from tic_tac_toe.game import EMPTY, PLAYER_O, PLAYER_X, new_board
from tic_tac_toe.minimax import WIN_SCORE, best_moves, score_move, score_position

X, O, _ = PLAYER_X, PLAYER_O, EMPTY


def test_takes_the_winning_move():
    board = [X, X, _, O, O, _, _, _, _]

    assert best_moves(board, X) == [2]


def test_blocks_the_opponents_winning_move():
    board = [X, X, _, _, O, _, _, _, _]

    assert best_moves(board, O) == [2]


def test_prefers_winning_now_over_blocking():
    board = [X, X, _, O, O, _, _, _, _]

    assert best_moves(board, O) == [5]


def test_empty_board_is_a_draw_and_every_move_is_equally_good():
    board = new_board()

    assert score_position(board, X) == 0
    assert best_moves(board, X) == list(range(9))


def test_answer_to_a_corner_opening_is_the_centre():
    board = [X, _, _, _, _, _, _, _, _]

    assert best_moves(board, O) == [4]


def test_immediate_win_scores_higher_than_a_later_win():
    # X can win at once on cell 8; cell 2 instead creates a double threat and wins later.
    board = [X, O, _, O, X, _, _, _, _]

    assert score_move(board, 8, X) == WIN_SCORE - 1
    assert 0 < score_move(board, 2, X) < score_move(board, 8, X)


def test_lost_position_has_negative_score():
    # O faces two threats (cells 2 and 6) and can only block one.
    board = [X, X, _, O, X, _, _, _, O]

    assert score_position(board, O) < 0


def test_full_board_has_no_best_move():
    board = [X, O, X, X, O, O, O, X, X]

    assert best_moves(board, X) == []
