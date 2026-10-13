"""The "teacher": finds the perfect moves by trying out every possible continuation.

Minimax idea: a move is as good as the position it leads to, assuming the opponent then
also plays his best move. Tic-tac-toe is small enough to search the whole game tree.

Scores are seen from the player whose turn it is:
    positive  = this player wins   (larger = wins sooner)
    0         = draw
    negative  = this player loses  (smaller = loses sooner)
"""

from tic_tac_toe.game import EMPTY, apply_move, find_winner, legal_moves

# Larger than the longest game (9 moves), so a win is always worth more than a draw.
WIN_SCORE = 10

# Remembers positions that were already solved; the same position is reached in many ways.
_score_cache: dict[tuple[tuple[int, ...], int], int] = {}


def score_position(board: list[int], player: int) -> int:
    """Return how good the position is for `player`, who is about to move."""
    winner = find_winner(board)
    if winner != EMPTY:
        # Only the previous move can have ended the game, so the player to move has lost.
        return -WIN_SCORE
    moves = legal_moves(board)
    if not moves:
        return 0

    key = (tuple(board), player)
    if key not in _score_cache:
        _score_cache[key] = max(score_move(board, cell, player) for cell in moves)
    return _score_cache[key]


def score_move(board: list[int], cell: int, player: int) -> int:
    """Return how good it is for `player` to play on `cell`."""
    opponent_score = score_position(apply_move(board, cell, player), -player)
    # What is good for the opponent is bad for us, hence the minus.
    score = -opponent_score
    # Move the score one step towards 0: a win in 1 move beats a win in 3 moves,
    # and a late defeat is better than an early one.
    if score > 0:
        return score - 1
    if score < 0:
        return score + 1
    return 0


def best_moves(board: list[int], player: int) -> list[int]:
    """Return every move with the highest score (often several are equally good)."""
    moves = legal_moves(board)
    if not moves:
        return []
    scores = {cell: score_move(board, cell, player) for cell in moves}
    best_score = max(scores.values())
    return [cell for cell in moves if scores[cell] == best_score]
