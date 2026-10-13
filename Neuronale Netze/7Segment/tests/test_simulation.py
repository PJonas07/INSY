import numpy as np

from seven_segment.dataset import load_inputs
from seven_segment.network import NeuralNetwork
from seven_segment.simulation import HIDDEN_LAYER, OUTPUT_LAYER, NodeStep, compute_steps


def test_one_step_per_hidden_and_output_neuron():
    steps = compute_steps(NeuralNetwork(), load_inputs()[3])

    assert [step.layer for step in steps] == [HIDDEN_LAYER] * 8 + [OUTPUT_LAYER] * 10


def test_step_by_step_matches_matrix_forward_pass():
    network = NeuralNetwork()
    segments = load_inputs()[5]

    steps = compute_steps(network, segments)
    result = network.forward(segments)

    hidden = [step.activation for step in steps[:8]]
    output = [step.activation for step in steps[8:]]
    assert np.allclose(hidden, result.hidden_activations)
    assert np.allclose(output, result.output_activations)


def test_output_steps_use_hidden_activations_as_inputs():
    steps = compute_steps(NeuralNetwork(), load_inputs()[0])

    hidden = [step.activation for step in steps[:8]]
    assert steps[8].inputs == hidden


def test_formula_shows_weights_bias_and_result():
    step = NodeStep(
        layer=HIDDEN_LAYER,
        index=1,
        inputs=[1.0, 0.0],
        weights=[0.5, -1.2],
        bias=0.3,
        weighted_sum=0.8,
        activation=0.69,
    )

    assert step.formula() == "h1 = σ(0.50·1.00 + (-1.20)·0.00 + 0.30) = σ(0.80) = 0.690"
