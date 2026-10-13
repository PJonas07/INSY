# Bereich: network + simulation

## Zweck
Das neuronale Netz und seine Knoten-für-Knoten-Darstellung.

## Schnittstelle
- `NeuralNetwork()` – Zufallsgewichte (Seed aus config).
- `forward(x) -> ForwardResult` – Summen und Aktivierungen beider Schichten.
- `compute_gradients(x, t)`, `train_step(x, t) -> loss`, `train(x, t, epochs) -> list[loss]`.
- `predict(segments) -> int`, `save(path, history)`, `load(path)`.
- `compute_steps(network, segments) -> list[NodeStep]` – 8 Hidden- und 10 Ausgabe-Schritte.

## Mathematik
- Neuron: `z = Σ wᵢ·xᵢ + b`, `a = σ(z) = 1 / (1 + e^−z)`.
- Fehler: `E = ½ · Σ (y − t)²`, gemittelt über die 10 Beispiele.
- Ausgabe-Delta: `δ_out = (y − t) · y · (1 − y)`.
- Hidden-Delta: `δ_hid = (δ_out · W_outᵀ) · h · (1 − h)`.
- Update: `W ← W − η · (Eingabeᵀ · δ)`, `b ← b − η · Σ δ`.
- Gewichte gespeichert als (von, nach): `weights_hidden[i, j]` = Eingang i → Hidden j.

## Stolperfallen
- `simulation.py` und `web/index.html` müssen dieselbe Rechnung machen wie `forward()`.

## Tests
`tests/test_network.py` (u. a. numerischer Gradienten-Check), `tests/test_simulation.py`.
