"""Break one forward pass into single-neuron steps, so the GUI can show each calculation.

NeuralNetwork.forward() computes a whole layer at once with a matrix product. Here the same
math is done neuron by neuron: weighted sum of the inputs plus bias, then sigmoid.
"""

from dataclasses import dataclass

import numpy as np

from seven_segment.network import NeuralNetwork, sigmoid

HIDDEN_LAYER = "hidden"
OUTPUT_LAYER = "output"


@dataclass
class NodeStep:
    """The calculation of a single neuron."""

    layer: str
    index: int
    inputs: list[float]
    weights: list[float]
    bias: float
    weighted_sum: float
    activation: float

    def formula(self) -> str:
        """Readable calculation, e.g. 'h1 = σ(0.50·1 + (-1.20)·0 + 0.30) = σ(0.80) = 0.690'."""
        name = f"h{self.index}" if self.layer == HIDDEN_LAYER else f"y{self.index}"
        terms = " + ".join(
            f"{_signed(weight)}·{value:.2f}"
            for weight, value in zip(self.weights, self.inputs, strict=True)
        )
        return (
            f"{name} = σ({terms} + {_signed(self.bias)})"
            f" = σ({self.weighted_sum:.2f}) = {self.activation:.3f}"
        )


def _signed(number: float) -> str:
    """Put negative numbers in brackets so '+ (-1.20)' stays readable."""
    return f"({number:.2f})" if number < 0 else f"{number:.2f}"


def _layer_steps(
    layer: str, inputs: np.ndarray, weights: np.ndarray, biases: np.ndarray
) -> list[NodeStep]:
    """Compute every neuron of one layer separately."""
    steps = []
    for index in range(weights.shape[1]):
        incoming_weights = weights[:, index]
        weighted_sum = float(np.dot(inputs, incoming_weights) + biases[index])
        steps.append(
            NodeStep(
                layer=layer,
                index=index,
                inputs=inputs.tolist(),
                weights=incoming_weights.tolist(),
                bias=float(biases[index]),
                weighted_sum=weighted_sum,
                activation=float(sigmoid(np.array(weighted_sum))),
            )
        )
    return steps


def compute_steps(network: NeuralNetwork, segments: np.ndarray) -> list[NodeStep]:
    """Return all neuron calculations in order: first every hidden, then every output neuron."""
    hidden_steps = _layer_steps(HIDDEN_LAYER, segments, network.weights_hidden, network.bias_hidden)
    hidden_activations = np.array([step.activation for step in hidden_steps])
    output_steps = _layer_steps(
        OUTPUT_LAYER, hidden_activations, network.weights_output, network.bias_output
    )
    return hidden_steps + output_steps
