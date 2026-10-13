# Tic-Tac-Toe mit einem neuronalen Netz

Ein kleines neuronales Netz lernt, in jeder Tic-Tac-Toe-Stellung einen guten Zug zu finden.
Sein Lehrer ist Minimax, ein Verfahren, das alle Spielverläufe durchprobiert und deshalb perfekt spielt.
Das Netz ist **selbst programmiert** (nur NumPy): Forward-Pass, Backpropagation, Gradientenabstieg.
Eine Website zeigt das Spiel, die Rechnung jedes Knotens und wie sich die Gewichte beim Training ändern.

```
Eingabe (9 Felder: 1 = ich, −1 = Gegner, 0 = leer)  →  Hidden (36 Neuronen, Sigmoid)  →  Ausgabe (9 Neuronen, eines pro Feld)
```

Ergebnis mit den Standardwerten: Das Netz trifft in 97,1 % der 4520 Stellungen einen besten Zug.
Wenn es beginnt, verliert es nie; als zweiter Spieler verliert es 21 von 497 möglichen Spielverläufen.

## Voraussetzungen

- macOS / Linux / Windows mit Python 3.12
- [uv](https://docs.astral.sh/uv/) (oder normales `python3.12 -m venv`)

## Setup

```bash
cd "TikTakToe"
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

## Starten

```bash
# 1. Netz trainieren (ca. 6 Sekunden; schreibt models/model.json und web/data.js)
.venv/bin/python -m tic_tac_toe.train

# 2. Website: web/index.html im Browser öffnen (Doppelklick genügt)
open web/index.html

# 3. In der Konsole gegen das Netz spielen
.venv/bin/python -m tic_tac_toe.play
```

`models/model.json` und `web/data.js` liegen schon bei – die Website läuft auch ohne Schritt 1.

### Bedienung der Website

| Aktion | Wirkung |
|---|---|
| leeres Feld anklicken | eigener Zug, danach zieht das Netz |
| **Neues Spiel** / **Netz beginnt** | Spiel neu starten, wahlweise mit dem Netz als X |
| Regler **Trainingsstand** | Netz zu einem früheren Zeitpunkt des Trainings ansehen (und dagegen spielen) |
| **Training abspielen** | alle Stände nacheinander – Kanten, Fehler und Trefferquote ändern sich |
| **Kanten zeigen: Änderung** | Kanten zeigen, wie stark sich jedes Gewicht seit dem Stand davor geändert hat |
| Knoten anklicken / Auswahlliste | Rechnung dieses Knotens und die Änderung seiner Gewichte |

## Testen und Linten

```bash
.venv/bin/pytest -q
.venv/bin/ruff check . && .venv/bin/ruff format --check .
```

## Projektstruktur

```
tic_tac_toe/
  config.py       Hyperparameter, Seed, Dateipfade
  game.py         Spielregeln
  minimax.py      perfekter Lehrer: beste Züge einer Stellung
  dataset.py      alle 4520 Stellungen mit ihren besten Zügen
  network.py      NeuralNetwork: forward, Backpropagation, speichern/laden
  simulation.py   Forward-Pass Knoten für Knoten
  evaluation.py   Zug des Netzes wählen, Spielstärke messen
  training.py     Trainingsschleife, merkt sich Gewichts-Stände
  train.py        Training in der Konsole
  export_html.py  schreibt web/data.js
  play.py         Konsolenspiel gegen das Netz
tests/            pytest-Tests
web/index.html    Website
docs/             Doku, Spezifikation, Entscheidungen, Protokoll
```

## Autor

Jonas Pichler
