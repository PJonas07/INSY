"""Train the network in the console, save it and export it for the HTML page.

Run from the project folder:  python -m tic_tac_toe.train
"""

from tic_tac_toe import config
from tic_tac_toe.dataset import load_dataset
from tic_tac_toe.evaluation import Outcomes, count_outcomes
from tic_tac_toe.export_html import export_training
from tic_tac_toe.game import PLAYER_O, PLAYER_X
from tic_tac_toe.network import NeuralNetwork
from tic_tac_toe.training import Snapshot, train_with_snapshots

PRINT_EVERY = 500


def print_progress(snapshots: list[Snapshot]) -> None:
    """Show how loss and best-move rate developed during the training."""
    print("Epoch | Loss    | Best moves")
    for snapshot in snapshots:
        if snapshot.epoch % PRINT_EVERY == 0:
            rate = snapshot.best_move_rate
            print(f"{snapshot.epoch:5d} | {snapshot.loss:.5f} | {rate:6.1%}")


def print_outcomes(label: str, outcomes: Outcomes) -> None:
    """Show the results of the network against every possible opponent."""
    print(
        f"Network plays {label}: {outcomes.wins} wins, {outcomes.draws} draws, "
        f"{outcomes.losses} losses"
    )


def main() -> None:
    inputs, targets = load_dataset()
    print(f"{len(inputs)} positions, {config.EPOCHS} epochs, learning rate {config.LEARNING_RATE}")
    network = NeuralNetwork()

    snapshots = train_with_snapshots(network, inputs, targets)
    print_progress(snapshots)

    outcomes_as_x = count_outcomes(network, PLAYER_X)
    outcomes_as_o = count_outcomes(network, PLAYER_O)
    print_outcomes("X (starts)", outcomes_as_x)
    print_outcomes("O (second)", outcomes_as_o)

    network.save(config.MODEL_PATH, [snapshot.loss for snapshot in snapshots])
    export_training(snapshots, outcomes_as_x, outcomes_as_o, len(inputs), config.WEB_DATA_PATH)
    print(f"\nSaved {config.MODEL_PATH}\nSaved {config.WEB_DATA_PATH}")


if __name__ == "__main__":
    main()
