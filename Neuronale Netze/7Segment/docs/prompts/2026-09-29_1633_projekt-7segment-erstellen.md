# Projekt 7Segment erstellen

**Datum:** 2026-09-29 16:33

## Prompt

> Mache mir im VS Code einen neuen Ordner mit Projekt. Name: Neuronale Netze; Bitte programmiere mir das Project 7Segment. Mache das ganze in Python. Auch eine Anzeige, Hintergrundsimulation wie es sich im Hintergrund die Knoten berechnen. Mache dann bitte am Schluss noch eine HTML zum visualisieren. Lese die Richtlinien im Ordner Claude. bitte ignoriere aber noch das git file

## Was gemacht wurde

- Rückfragen: Kategorie Schule, Aufgabe 7 Segmente → Ziffer, nur NumPy, keine Lehrkraft-Vorgaben.
- Python 3.12.14 über `uv` installiert, venv mit numpy/pytest/ruff.
- Netz 7 → 8 → 10 mit Backpropagation (NumPy), Training erkennt alle 10 Ziffern.
- Schritt-Simulation (`simulation.py`) für die Knoten-für-Knoten-Anzeige.
- tkinter-App: klickbare Anzeige, Netzgraph, Formeln pro Knoten, Animation, Live-Training mit Fehlerkurve.
- HTML-Visualisierung `web/index.html` (hell/dunkel, responsiv, Tastatur).
- 20 pytest-Tests, ruff sauber; Doku, Spec, ADR, Protokoll.

## Geänderte Dateien

- `seven_segment/*.py` – neu
- `tests/*.py` – neu
- `web/index.html`, `web/data.js` – neu
- `models/model.json` – neu (generiert)
- `README.md`, `CLAUDE.md`, `pyproject.toml`, `requirements.txt`, `.claude/settings.json` – neu
- `docs/DOKU.md`, `docs/bereiche/network.md`, `docs/spec/anforderungen.md`, `docs/decisions/0001-numpy-eigenes-netz.md`, `docs/phase-log.md` – neu

## Offen

- GUI einmal selbst öffnen und ansehen (Prüfliste in der Antwort).
- Phase-Log: „Stunden“ und „Selbst entschieden“ selbst ausfüllen.

## Rückfrage

> Bitte installiere einfach 3.12 selber

→ uv + Python 3.12.14 installiert, danach gebaut.
