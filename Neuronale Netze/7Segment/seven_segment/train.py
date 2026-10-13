"""Train the network in the console, save it and export it for the HTML page.

Run from the project folder:  python -m seven_segment.train
"""

import numpy as np

from seven_segment import config
from seven_segment.dataset import load_inputs, load_targets
from seven_segment.export_html import export_model
from seven_segment.network import NeuralNetwork

PRINT_EVERY = 500


def print_predictions(network: NeuralNetwork, inputs: np.ndarray) -> None:
    """Show for every digit which digit the network recognises and how sure it is."""
    print("\nDigit | Segments | Recognised | Confidence")
    for digit, segments in enumerate(inputs):
        outputs = network.forward(segments).output_activations
        recognised = int(np.argmax(outputs))
        pattern = "".join(str(int(value)) for value in segments)
        mark = "ok" if recognised == digit else "WRONG"
        confidence = outputs[recognised]
        print(f"  {digit}   | {pattern}  |     {recognised}      | {confidence:.3f}  {mark}")


def main() -> None:
    inputs = load_inputs()
    targets = load_targets()
    network = NeuralNetwork()

    losses = []
    for epoch in range(1, config.EPOCHS + 1):
        losses.append(network.train_step(inputs, targets))
        if epoch % PRINT_EVERY == 0:
            print(f"Epoch {epoch:5d}  loss {losses[-1]:.5f}")

    print_predictions(network, inputs)

    loss_history = losses[:: config.LOSS_HISTORY_STEP]
    network.save(config.MODEL_PATH, loss_history)
    export_model(network, loss_history, config.WEB_DATA_PATH)
    print(f"\nSaved {config.MODEL_PATH}\nSaved {config.WEB_DATA_PATH}")


if __name__ == "__main__":
    main()
