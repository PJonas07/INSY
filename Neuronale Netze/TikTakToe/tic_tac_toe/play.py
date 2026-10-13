"""Play tic-tac-toe against the trained network in the console.

Run from the project folder:  python -m tic_tac_toe.play
"""

from tic_tac_toe import config
from tic_tac_toe.evaluation import choose_move
from tic_tac_toe.game import (
    EMPTY,
    PLAYER_O,
    PLAYER_X,
    apply_move,
    find_winner,
    format_board,
    is_game_over,
    legal_moves,
    new_board,
)
from tic_tac_toe.network import NeuralNetwork


def parse_move(text: str, board: list[int]) -> int | None:
    """Return the chosen cell, or None if the text is not a free cell number."""
    if not text.strip().isdigit():
        return None
    cell = int(text)
    if cell not in legal_moves(board):
        return None
    return cell


def ask_for_move(board: list[int]) -> int:
    """Ask the human until a free cell number is entered."""
    while True:
        cell = parse_move(input("Your move (number of a free cell): "), board)
        if cell is not None:
            return cell
        print("Please enter the number of a free cell.")


def describe_result(board: list[int], human: int) -> str:
    """Return the final message from the human's point of view."""
    winner = find_winner(board)
    if winner == EMPTY:
        return "Draw."
    return "You win!" if winner == human else "The network wins."


def main() -> None:
    if not config.MODEL_PATH.exists():
        raise SystemExit("No trained model found. Run 'python -m tic_tac_toe.train' first.")
    network, _ = NeuralNetwork.load(config.MODEL_PATH)

    wants_to_start = input("Do you want to start? [y/n] ").strip().lower() != "n"
    human = PLAYER_X if wants_to_start else PLAYER_O
    board = new_board()
    player = PLAYER_X

    while not is_game_over(board):
        if player == human:
            print("\n" + format_board(board))
            cell = ask_for_move(board)
        else:
            cell = choose_move(network, board, player)
            print(f"\nThe network plays cell {cell}.")
        board = apply_move(board, cell, player)
        player = -player

    print("\n" + format_board(board))
    print(describe_result(board, human))


if __name__ == "__main__":
    main()
