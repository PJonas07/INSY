# CLAUDE.md – 7Segment (Neuronale Netze)

Kategorie: Schule
Team: allein (Jonas)
Abgabe / Deadline: –
Git: ja – seit 2026-10-13 Teil des Repositorys `INSY` (Wurzel: Ordner `Insy`, zwei Ebenen höher); nie direkt auf `main`

Neuronales Netz (7 → 8 → 10), das die Ziffer auf einer 7-Segment-Anzeige erkennt. Selbst programmiert mit NumPy (Forward-Pass + Backpropagation), inkl. Desktop-Visualisierung (tkinter) und HTML-Seite. Ziel: jeden Rechenschritt erklären können.

## Quelle der Wahrheit

| Datei | Inhalt |
|---|---|
| `docs/spec/anforderungen.md` | Anforderungen |
| `docs/DOKU.md` | Karte + aktueller Stand |
| `docs/phase-log.md` | Arbeitsprotokoll |

**Vor der Umsetzung den relevanten Spec-Abschnitt lesen.** Widerspruch oder Lücke → stoppen und fragen.

## Tech-Stack

- Python 3.12 (über `uv` installiert), venv in `.venv`
- NumPy für die Mathematik, tkinter (Standardbibliothek) für die GUI, HTML/CSS/JS ohne Frameworks
- Erlaubte Dependencies: numpy, pytest, ruff. Keine weitere ohne Rücksprache.

## Architektur

```
seven_segment/   Python-Paket (config, dataset, network, simulation, train, gui, export_html)
tests/           pytest
models/          trainiertes Modell (model.json, generiert)
web/             index.html + data.js (generiert)
docs/            DOKU, Spec, ADRs, Protokoll, Prompts
```

Regeln:
- Hyperparameter nur in `seven_segment/config.py`.
- `simulation.py` rechnet dieselbe Mathematik wie `network.forward()`, nur neuronweise – beide müssen übereinstimmen (Test vorhanden). `web/index.html` spiegelt `simulation.py` in JavaScript.

## Bauen, Testen, Linten

```bash
~/.local/bin/uv venv --python 3.12 .venv
~/.local/bin/uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m seven_segment.train
.venv/bin/pytest -q
.venv/bin/ruff check . && .venv/bin/ruff format --check .
```

## Projektspezifische Regeln

- UI-Sprache: Deutsch
- Ordner: `VS Code/Insy/Neuronale Netze/7Segment` – als eigenen Ordner öffnen.
