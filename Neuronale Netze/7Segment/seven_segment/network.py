"""A small fully connected neural network (7 -> hidden -> 10) written with NumPy only.

Notation used in comments:
    x  inputs (segments)            shape (samples, 7)
    h  hidden activations           shape (samples, hidden)
    y  output activations           shape (samples, 10)
    t  targets (one-hot digit)      shape (samples, 10)

Weight matrices are stored as (from_layer, to_layer), so weights_hidden[i, j] is the
weight of the edge from input i to hidden neuron j.
"""

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from seven_segment import config


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Squash any number into (0, 1): sigma(z) = 1 / (1 + e^-z)."""
    return 1.0 / (1.0 + np.exp(-z))


@dataclass
class ForwardResult:
    """All intermediate values of one forward pass (needed for backprop and display)."""

    inputs: np.ndarray
    hidden_sums: np.ndarray
    hidden_activations: np.ndarray
    output_sums: np.ndarray
    output_activations: np.ndarray


class NeuralNetwork:
    """Two-layer network trained with backpropagation and gradient descent."""

    def __init__(
        self,
        input_size: int = config.INPUT_SIZE,
        hidden_size: int = config.HIDDEN_SIZE,
        output_size: int = config.OUTPUT_SIZE,
        seed: int = config.RANDOM_SEED,
    ) -> None:
        rng = np.random.default_rng(seed)
        low, high = -config.INIT_RANGE, config.INIT_RANGE
        self.weights_hidden = rng.uniform(low, high, (input_size, hidden_size))
        self.bias_hidden = rng.uniform(low, high, hidden_size)
        self.weights_output = rng.uniform(low, high, (hidden_size, output_size))
        self.bias_output = rng.uniform(low, high, output_size)

    # ------------------------------------------------------------------ forward

    def forward(self, inputs: np.ndarray) -> ForwardResult:
        """Compute the network output for one sample (shape (7,)) or many (shape (n, 7))."""
        hidden_sums = inputs @ self.weights_hidden + self.bias_hidden
        hidden_activations = sigmoid(hidden_sums)
        output_sums = hidden_activations @ self.weights_output + self.bias_output
        output_activations = sigmoid(output_sums)
        return ForwardResult(
            inputs, hidden_sums, hidden_activations, output_sums, output_activations
        )

    def predict(self, segments: np.ndarray) -> int:
        """Return the digit whose output neuron is most active."""
        return int(np.argmax(self.forward(segments).output_activations))

    # ------------------------------------------------------------------ training

    @staticmethod
    def loss(outputs: np.ndarray, targets: np.ndarray) -> float:
        """Error E = 1/2 * sum((y - t)^2), averaged over all samples."""
        return float(0.5 * np.sum((outputs - targets) ** 2) / len(targets))

    def compute_gradients(
        self, inputs: np.ndarray, targets: np.ndarray
    ) -> tuple[ForwardResult, dict[str, np.ndarray]]:
        """Backpropagation: derivative of the loss with respect to every weight and bias."""
        result = self.forward(inputs)
        sample_count = len(inputs)

        # Output layer: dE/dy = (y - t), sigmoid'(z) = y * (1 - y).
        y = result.output_activations
        delta_output = (y - targets) * y * (1 - y) / sample_count

        # Hidden layer: error flows back through the output weights.
        h = result.hidden_activations
        delta_hidden = (delta_output @ self.weights_output.T) * h * (1 - h)

        gradients = {
            "weights_output": h.T @ delta_output,
            "bias_output": delta_output.sum(axis=0),
            "weights_hidden": inputs.T @ delta_hidden,
            "bias_hidden": delta_hidden.sum(axis=0),
        }
        return result, gradients

    def train_step(
        self, inputs: np.ndarray, targets: np.ndarray, learning_rate: float = config.LEARNING_RATE
    ) -> float:
        """One gradient descent step on all samples; returns the loss before the step."""
        result, gradients = self.compute_gradients(inputs, targets)
        self.weights_output -= learning_rate * gradients["weights_output"]
        self.bias_output -= learning_rate * gradients["bias_output"]
        self.weights_hidden -= learning_rate * gradients["weights_hidden"]
        self.bias_hidden -= learning_rate * gradients["bias_hidden"]
        return self.loss(result.output_activations, targets)

    def train(
        self, inputs: np.ndarray, targets: np.ndarray, epochs: int = config.EPOCHS
    ) -> list[float]:
        """Train for a number of epochs and return the loss of every epoch."""
        return [self.train_step(inputs, targets) for _ in range(epochs)]

    # ------------------------------------------------------------------ save / load

    def to_dict(self) -> dict[str, list]:
        """Weights as plain lists, so they can be written to JSON."""
        return {
            "weights_hidden": self.weights_hidden.tolist(),
            "bias_hidden": self.bias_hidden.tolist(),
            "weights_output": self.weights_output.tolist(),
            "bias_output": self.bias_output.tolist(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, list]) -> "NeuralNetwork":
        """Rebuild a network from the output of to_dict()."""
        weights_hidden = np.array(data["weights_hidden"], dtype=float)
        weights_output = np.array(data["weights_output"], dtype=float)
        network = cls(
            input_size=weights_hidden.shape[0],
            hidden_size=weights_hidden.shape[1],
            output_size=weights_output.shape[1],
        )
        network.weights_hidden = weights_hidden
        network.bias_hidden = np.array(data["bias_hidden"], dtype=float)
        network.weights_output = weights_output
        network.bias_output = np.array(data["bias_output"], dtype=float)
        return network

    def save(self, path: Path, loss_history: list[float]) -> None:
        """Write weights and the (thinned out) loss curve to a JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {"network": self.to_dict(), "loss_history": loss_history}
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> tuple["NeuralNetwork", list[float]]:
        """Read a file written by save()."""
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls.from_dict(data["network"]), data["loss_history"]
