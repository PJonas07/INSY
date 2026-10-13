import numpy as np

from tic_tac_toe.dataset import load_dataset
from tic_tac_toe.export_html import FORWARD_CHECK_INPUTS, build_forward_check, round_weights
from tic_tac_toe.network import NeuralNetwork
from tic_tac_toe.training import train_with_snapshots

INPUTS, TARGETS = load_dataset()
SHORT_TRAINING_EPOCHS = 300
RATE_AFTER_SHORT_TRAINING = 0.7


def test_snapshots_are_taken_before_training_and_every_nth_epoch():
    snapshots = train_with_snapshots(NeuralNetwork(), INPUTS, TARGETS, epochs=6, snapshot_every=2)

    assert [snapshot.epoch for snapshot in snapshots] == [0, 2, 4, 6]


def test_first_snapshot_holds_the_untrained_weights():
    network = NeuralNetwork()
    start_weights = network.to_dict()

    snapshots = train_with_snapshots(network, INPUTS, TARGETS, epochs=2, snapshot_every=1)

    assert snapshots[0].weights == start_weights


def test_weights_differ_between_snapshots():
    snapshots = train_with_snapshots(NeuralNetwork(), INPUTS, TARGETS, epochs=2, snapshot_every=1)

    assert snapshots[0].weights != snapshots[1].weights
    assert snapshots[1].weights != snapshots[2].weights


def test_training_learns_to_find_best_moves():
    snapshots = train_with_snapshots(
        NeuralNetwork(), INPUTS, TARGETS, epochs=SHORT_TRAINING_EPOCHS, snapshot_every=100
    )

    assert snapshots[-1].loss < snapshots[0].loss
    assert snapshots[-1].best_move_rate > snapshots[0].best_move_rate
    assert snapshots[-1].best_move_rate > RATE_AFTER_SHORT_TRAINING


def test_round_weights_keeps_names_and_shapes():
    weights = NeuralNetwork().to_dict()

    rounded = round_weights(weights)

    assert rounded.keys() == weights.keys()
    assert np.array(rounded["weights_hidden"]).shape == np.array(weights["weights_hidden"]).shape
    assert np.allclose(rounded["weights_hidden"], weights["weights_hidden"], atol=1e-4)


def test_forward_check_matches_the_network():
    network = NeuralNetwork()

    check = build_forward_check(network.to_dict())

    expected = network.forward(np.array(FORWARD_CHECK_INPUTS, dtype=float)).output_activations
    assert check["inputs"] == FORWARD_CHECK_INPUTS
    assert np.allclose(check["outputs"], expected)
