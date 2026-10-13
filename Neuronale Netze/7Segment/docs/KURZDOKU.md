# 7Segment – Kurzdoku

Stand: 2026-10-13 · Jonas Pichler und Petra Bernroitner 

## Was gemacht wurde

Ein neuronales Netz erkennt, welche Ziffer (0–9) eine 7-Segment-Anzeige zeigt. Es bekommt die 7 Segmente a–g (ein = 1, aus = 0) und gibt die Ziffer aus. Das Netz ist selbst programmiert (nur NumPy, kein ML-Framework). Eine Desktop-App und eine HTML-Seite zeigen, wie jeder Knoten seinen Wert berechnet.

## Wie es umgesetzt ist

1. **Trainingsdaten** (`dataset.py`): eine Tabelle mit 10 Zeilen – für jede Ziffer, welche Segmente leuchten. Ziel ist pro Ziffer eine 1 beim richtigen Ausgang, sonst 0.
2. **Netz** (`network.py`): 7 Eingänge → 8 Hidden-Neuronen → 10 Ausgänge (einer pro Ziffer), überall Sigmoid.
   - Neuron: `z = Σ w·x + b`, `a = 1 / (1 + e^−z)`
   - Fehler: `E = ½ · Σ (y − t)²`
   - Lernen: Backpropagation und Gradientenabstieg, Lernrate 2, 3000 Epochen, Seed 42.
   - Erkannte Ziffer = Ausgang mit dem höchsten Wert.
3. **Schritt-Simulation** (`simulation.py`): rechnet dasselbe wie das Netz, aber Knoten für Knoten (8 Hidden + 10 Ausgänge = 18 Schritte) und liefert zu jedem Schritt die Formel mit Zahlen.
4. **Training** (`train.py`): trainiert in der Konsole (unter 1 Sekunde), speichert das Modell (`models/model.json`) und die Daten für die HTML-Seite (`web/data.js`).
5. **Desktop-App** (`gui.py`, tkinter): klickbare Anzeige, Netzgraph (Knotenfarbe = Aktivierung, Kanten = Gewicht), Berechnung Schritt für Schritt oder als Animation, Live-Training mit Fehlerkurve.
6. **HTML-Seite** (`web/index.html`, ohne Frameworks): dieselbe Anzeige und Schritt-Berechnung im Browser mit den trainierten Gewichten, dazu die Fehlerkurve des Trainings. Kein Live-Training.

## Ergebnis

| Messung | Wert |
|---|---|
| Richtig erkannte Ziffern | 10 von 10 |
| Sicherheit (niedrigster Wert des richtigen Ausgangs) | 0,914 |
| Fehler am Anfang → am Ende | 1,130 → 0,004 |

Einschränkung: Auch bei einem Muster, das keine Ziffer ist (z. B. nur Segment a), nennt das Netz eine Ziffer – es kennt keine Klasse „keine Ziffer“.

## Qualität

- 20 automatische Tests (u. a. Vergleich der Backpropagation mit einem numerisch berechneten Gradienten; Schritt-Simulation = Netz), Linter ruff ohne Meldung.
- Desktop-App und HTML-Seite werden von Hand geprüft.

## Starten

```bash
.venv/bin/python -m seven_segment.train   # trainieren
.venv/bin/python -m seven_segment.gui     # Desktop-App
open web/index.html                       # HTML-Seite
```

## KI-Einsatz

Planung, Code, Tests und Doku wurden mit Claude erstellt. Die Entscheidungen dazu stehen in `docs/DOKU.md` und `docs/decisions/`.
