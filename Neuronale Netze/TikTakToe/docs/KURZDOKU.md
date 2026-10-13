# TikTakToe – Kurzdoku

Stand: 2026-10-13 · Jonas Pichler und Sarah Krottenhammer 

## Was gemacht wurde

Ein neuronales Netz spielt Tic-Tac-Toe. Es bekommt das Spielfeld und sagt für jedes der 9 Felder, wie gut ein Zug dort ist. Das Netz ist selbst programmiert (nur NumPy, kein ML-Framework), gleich aufgebaut wie im Projekt 7Segment. Eine Website dient als Oberfläche und zeigt auch, wie sich die Gewichte beim Training ändern.

## Wie es umgesetzt ist

1. **Spielregeln** (`game.py`): Feld als Liste mit 9 Zahlen (1 = X, −1 = O, 0 = leer), Sieger erkennen, freie Felder, Zug setzen.
2. **Lehrer** (`minimax.py`): Minimax probiert alle Spielverläufe durch und kennt deshalb zu jeder Stellung die besten Züge. Schnelle Siege zählen mehr als späte.
3. **Trainingsdaten** (`dataset.py`): alle 4520 Stellungen, die in einem Spiel vorkommen können.
   - Eingabe: das Feld aus Sicht des Spielers am Zug (1 = eigener Stein, −1 = Gegner, 0 = leer). So reicht ein Netz für X und O.
   - Ziel: 1 für jedes Feld, das ein bester Zug ist, sonst 0.
4. **Netz** (`network.py`): 9 Eingänge → 36 Hidden-Neuronen → 9 Ausgänge, überall Sigmoid.
   - Neuron: `z = Σ w·x + b`, `a = 1 / (1 + e^−z)`
   - Fehler: `E = ½ · Σ (y − t)²`
   - Lernen: Backpropagation und Gradientenabstieg, Lernrate 10, 5000 Epochen, Seed 42.
5. **Training** (`training.py`, `train.py`): Alle 100 Epochen wird eine Kopie der Gewichte gemerkt (51 Stände). Am Ende werden das Modell (`models/model.json`) und die Daten für die Website (`web/data.js`) geschrieben.
6. **Zug wählen** (`evaluation.py`): Das Netz spielt das leere Feld mit der höchsten Ausgabe.
7. **Website** (`web/index.html`, ohne Frameworks): Spiel gegen das Netz, Netzgraph, Rechnung jedes Knotens als Formel. Ein Regler spielt die 51 Stände ab; die Kanten zeigen wahlweise das Gewicht oder dessen Änderung seit dem Stand davor. Die Website trainiert nicht selbst, sie zeigt die Stände aus Python.
8. **Konsole** (`play.py`): dasselbe Spiel im Terminal.

## Ergebnis

| Messung | Wert |
|---|---|
| Beste Züge getroffen | 97,1 % von 4520 Stellungen |
| Netz beginnt (X) | 72 Siege, 4 Remis, 0 Niederlagen |
| Netz ist Zweiter (O) | 344 Siege, 132 Remis, 21 Niederlagen |

Gezählt sind alle Spielverläufe gegen jeden möglichen Gegnerzug. Das Netz ist also gut, aber nicht perfekt: Als zweiter Spieler kann man es schlagen.

## Qualität

- 62 automatische Tests (u. a. Vergleich der Backpropagation mit einem numerisch berechneten Gradienten), Linter ruff ohne Meldung.
- Die Website vergleicht beim Laden ihre JavaScript-Rechnung mit einem Beispiel aus Python.
- Website von Hand geprüft (Prüfliste im Prompt-Protokoll).

## Starten

```bash
.venv/bin/python -m tic_tac_toe.train   # trainieren
open web/index.html                     # Website
.venv/bin/python -m tic_tac_toe.play    # Konsolenspiel
```

## KI-Einsatz

Planung, Code, Tests und Doku wurden mit Claude erstellt. Die Entscheidungen dazu stehen in `docs/DOKU.md` und `docs/decisions/`.
