# 7-Segment-Erkennung mit einem neuronalen Netz

Ein kleines neuronales Netz lernt, welche Ziffer (0–9) eine 7-Segment-Anzeige zeigt.
Das Netz ist **selbst programmiert** (nur NumPy): Forward-Pass, Backpropagation, Gradientenabstieg.
Eine Desktop-App und eine HTML-Seite zeigen, wie jeder Knoten seinen Wert berechnet.

```
Eingabe (7 Segmente a–g)  →  Hidden (8 Neuronen, Sigmoid)  →  Ausgabe (10 Neuronen, eine pro Ziffer)
```

## Voraussetzungen

- macOS / Linux / Windows mit Python 3.12
- [uv](https://docs.astral.sh/uv/) (oder normales `python3.12 -m venv`)

## Setup

```bash
cd "7Segment"
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

## Starten

```bash
# 1. Netz trainieren (speichert models/model.json und web/data.js)
.venv/bin/python -m seven_segment.train

# 2. Desktop-App mit Live-Visualisierung
.venv/bin/python -m seven_segment.gui

# 3. HTML-Visualisierung: web/index.html im Browser öffnen (Doppelklick genügt)
open web/index.html
```

### Bedienung der Desktop-App

| Aktion | Wirkung |
|---|---|
| Segment anklicken / Taste a–g | Segment ein/aus, Netz rechnet sofort neu |
| Ziffer-Button / Taste 0–9 | Muster dieser Ziffer laden |
| **Nächster Schritt** / Leertaste | nächsten Knoten berechnen, Rechnung wird angezeigt |
| **Animation abspielen** | alle 18 Knoten nacheinander berechnen |
| **Training starten** | trainiert live, Gewichte und Fehlerkurve ändern sich sichtbar |
| **Netz zurücksetzen** | zufällige Startgewichte – danach „Training starten“ zum Zusehen |

## Testen und Linten

```bash
.venv/bin/pytest -q
.venv/bin/ruff check . && .venv/bin/ruff format --check .
```

## Projektstruktur

```
seven_segment/
  config.py       Hyperparameter, Seed, Dateipfade
  dataset.py      Segment-Tabelle der Ziffern 0–9
  network.py      NeuralNetwork: forward, Backpropagation, train, speichern/laden
  simulation.py   Forward-Pass Knoten für Knoten (für die Anzeige)
  train.py        Training in der Konsole
  gui.py          Desktop-App (tkinter)
  export_html.py  schreibt web/data.js
tests/            pytest-Tests
web/index.html    HTML-Visualisierung
docs/             Doku, Spezifikation, Entscheidungen, Protokoll
```

## Autor

Jonas Pichler
