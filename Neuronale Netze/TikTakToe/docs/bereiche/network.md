# Bereich: network + simulation + training

## Zweck

Das neuronale Netz, seine Knoten-für-Knoten-Darstellung und die Trainingsschleife, die Gewichts-Stände merkt.

## Schnittstelle nach außen

- `NeuralNetwork()` – Zufallsgewichte (Seed aus config).
- `forward(x) -> ForwardResult` – Summen und Aktivierungen beider Schichten.
- `compute_gradients(x, t)`, `train_step(x, t) -> loss`, `train(x, t, epochs) -> list[loss]`.
- `to_dict()`, `from_dict()`, `save(path, loss_history)`, `load(path)`.
- `compute_steps(network, inputs) -> list[NodeStep]` – 36 Hidden- und 9 Ausgabe-Schritte.
- `train_with_snapshots(network, x, t, epochs, snapshot_every) -> list[Snapshot]` – Stand vor dem Training und nach jeder n-ten Epoche (Epoche, Fehler, Anteil bester Züge, Kopie der Gewichte).

## Mathematik

- Neuron: `z = Σ wᵢ·xᵢ + b`, `a = σ(z) = 1 / (1 + e^−z)`.
- Fehler: `E = ½ · Σ (y − t)²`, gemittelt über alle 4520 Stellungen.
- Ausgabe-Delta: `δ_out = (y − t) · y · (1 − y)`.
- Hidden-Delta: `δ_hid = (δ_out · W_outᵀ) · h · (1 − h)`.
- Update: `W ← W − η · (Eingabeᵀ · δ)`, `b ← b − η · Σ δ`.
- Gewichte gespeichert als (von, nach): `weights_hidden[i, j]` = Eingang i → Hidden j.

## Wichtige Details / Stolperfallen

- `network.py` und `simulation.py` sind bis auf die Docstrings identisch mit 7Segment.
- `simulation.py` und `web/index.html` müssen dieselbe Rechnung machen wie `forward()`.
- `to_dict()` erzeugt neue Listen – ein Snapshot ändert sich deshalb nicht mehr, wenn weitertrainiert wird.
- Die Lernrate 10 wirkt hoch; der Gradient ist aber durch 4520 Stellungen geteilt.

## Tests

`tests/test_network.py` (u. a. numerischer Gradienten-Check), `tests/test_simulation.py`, `tests/test_training.py`.
