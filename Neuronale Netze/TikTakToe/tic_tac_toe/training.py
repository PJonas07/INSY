"""The training loop, which also records how the weights change over time."""

from dataclasses import dataclass

import numpy as np

from tic_tac_toe import config
from tic_tac_toe.evaluation import best_move_rate
from tic_tac_toe.network import NeuralNetwork


@dataclass
class Snapshot:
    """The state of the network at one moment of the training."""

    epoch: int
    loss: float
    best_move_rate: float
    weights: dict[str, list]


def take_snapshot(
    network: NeuralNetwork, inputs: np.ndarray, targets: np.ndarray, epoch: int
) -> Snapshot:
    """Copy the current weights and measure how good the network is right now."""
    outputs = network.forward(inputs).output_activations
    return Snapshot(
        epoch=epoch,
        loss=network.loss(outputs, targets),
        best_move_rate=best_move_rate(network, inputs, targets),
        weights=network.to_dict(),
    )


def train_with_snapshots(
    network: NeuralNetwork,
    inputs: np.ndarray,
    targets: np.ndarray,
    epochs: int = config.EPOCHS,
    snapshot_every: int = config.SNAPSHOT_EVERY,
) -> list[Snapshot]:
    """Train the network and return its state before training and after every n-th epoch."""
    snapshots = [take_snapshot(network, inputs, targets, epoch=0)]
    for epoch in range(1, epochs + 1):
        network.train_step(inputs, targets)
        if epoch % snapshot_every == 0:
            snapshots.append(take_snapshot(network, inputs, targets, epoch))
    return snapshots
