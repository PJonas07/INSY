import numpy as np

from tic_tac_toe import config
from tic_tac_toe.network import NeuralNetwork
from tic_tac_toe.simulation import HIDDEN_LAYER, OUTPUT_LAYER, NodeStep, compute_steps

HIDDEN = config.HIDDEN_SIZE
# I hold cells 0 and 4, the opponent holds 1 and 8.
BOARD = np.array([1.0, -1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, -1.0])


def test_one_step_per_hidden_and_output_neuron():
    steps = compute_steps(NeuralNetwork(), BOARD)

    assert [step.layer for step in steps] == [HIDDEN_LAYER] * HIDDEN + [OUTPUT_LAYER] * 9


def test_step_by_step_matches_matrix_forward_pass():
    network = NeuralNetwork()
    steps = compute_steps(network, BOARD)
    result = network.forward(BOARD)

    hidden = [step.activation for step in steps[:HIDDEN]]
    output = [step.activation for step in steps[HIDDEN:]]
    assert np.allclose(hidden, result.hidden_activations)
    assert np.allclose(output, result.output_activations)


def test_output_steps_use_hidden_activations_as_inputs():
    steps = compute_steps(NeuralNetwork(), BOARD)

    hidden = [step.activation for step in steps[:HIDDEN]]
    assert steps[HIDDEN].inputs == hidden


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
