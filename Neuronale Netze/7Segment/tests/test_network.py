import numpy as np

from seven_segment.dataset import load_inputs, load_targets
from seven_segment.network import NeuralNetwork, sigmoid

GRADIENT_EPSILON = 1e-6
GRADIENT_TOLERANCE = 1e-6


def test_sigmoid_of_zero_is_one_half():
    assert sigmoid(np.array(0.0)) == 0.5


def test_sigmoid_stays_between_zero_and_one():
    values = sigmoid(np.array([-50.0, -1.0, 1.0, 50.0]))

    assert np.all(values >= 0) and np.all(values <= 1)


def test_forward_single_sample_has_ten_outputs():
    network = NeuralNetwork()

    result = network.forward(load_inputs()[0])

    assert result.hidden_activations.shape == (8,)
    assert result.output_activations.shape == (10,)


def test_forward_batch_has_one_output_row_per_sample():
    network = NeuralNetwork()

    result = network.forward(load_inputs())

    assert result.output_activations.shape == (10, 10)


def test_same_seed_gives_same_weights():
    first = NeuralNetwork(seed=1)
    second = NeuralNetwork(seed=1)

    assert np.array_equal(first.weights_hidden, second.weights_hidden)


def test_backprop_matches_numerical_gradient():
    """Compare every analytic gradient with (E(w + eps) - E(w - eps)) / (2 * eps)."""
    network = NeuralNetwork()
    inputs, targets = load_inputs(), load_targets()

    _, gradients = network.compute_gradients(inputs, targets)

    for name, analytic in gradients.items():
        parameter = getattr(network, name)
        numeric = np.zeros_like(parameter)
        for index in np.ndindex(parameter.shape):
            original = parameter[index]
            parameter[index] = original + GRADIENT_EPSILON
            loss_plus = network.loss(network.forward(inputs).output_activations, targets)
            parameter[index] = original - GRADIENT_EPSILON
            loss_minus = network.loss(network.forward(inputs).output_activations, targets)
            parameter[index] = original
            numeric[index] = (loss_plus - loss_minus) / (2 * GRADIENT_EPSILON)
        assert np.allclose(analytic, numeric, atol=GRADIENT_TOLERANCE), name


def test_training_reduces_loss():
    network = NeuralNetwork()

    losses = network.train(load_inputs(), load_targets(), epochs=200)

    assert losses[-1] < losses[0]


def test_trained_network_recognises_every_digit():
    network = NeuralNetwork()
    inputs = load_inputs()

    network.train(inputs, load_targets())

    predictions = [network.predict(segments) for segments in inputs]
    assert predictions == list(range(10))


def test_save_and_load_keep_weights_and_history(tmp_path):
    network = NeuralNetwork()
    path = tmp_path / "model.json"

    network.save(path, [0.5, 0.25])
    loaded, history = NeuralNetwork.load(path)

    assert np.allclose(loaded.weights_output, network.weights_output)
    assert np.allclose(loaded.bias_hidden, network.bias_hidden)
    assert history == [0.5, 0.25]
