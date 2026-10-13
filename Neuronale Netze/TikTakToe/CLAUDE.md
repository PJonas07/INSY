# CLAUDE.md – TikTakToe (Neuronale Netze)

Kategorie: Schule
Team: allein (Jonas)
Abgabe / Deadline: –
Git: ja – Teil des Repositorys `INSY` (Wurzel: Ordner `Insy`, zwei Ebenen höher)

Neuronales Netz, das Tic-Tac-Toe spielt: Es bekommt das Spielfeld (9 Felder) und gibt aus, welches Feld der beste Zug ist. Selbst programmiert mit NumPy (Forward-Pass + Backpropagation) wie im Projekt 7Segment. Oberfläche ist eine Website, die auch zeigt, wie sich die Gewichte beim Training ändern. Ziel: jeden Rechenschritt erklären können.

## Quelle der Wahrheit

| Datei | Inhalt |
|---|---|
| `docs/spec/anforderungen.md` | Anforderungen |
| `docs/DOKU.md` | Karte + aktueller Stand |
| `docs/phase-log.md` | Arbeitsprotokoll |

**Vor der Umsetzung den relevanten Spec-Abschnitt lesen.** Widerspruch oder Lücke → stoppen und fragen.

## Tech-Stack

- Python 3.12 (über `uv` installiert), venv in `.venv`
- NumPy für die Mathematik, HTML/CSS/JS ohne Frameworks für die Oberfläche
- Erlaubte Dependencies: numpy, pytest, ruff (dieselben wie 7Segment). Keine weitere ohne Rücksprache.

## Architektur

```
tic_tac_toe/   Python-Paket (config, game, minimax, dataset, network, simulation,
               evaluation, training, train, export_html, play)
tests/         pytest
models/        trainiertes Modell (model.json, generiert)
web/           index.html + data.js (generiert)
docs/          DOKU, Spec, ADRs, Protokoll, Prompts
```

Regeln:
- Hyperparameter nur in `tic_tac_toe/config.py`.
- `game.py` kennt kein Netz, `minimax.py` kennt kein Netz – das Netz lernt nur aus `dataset.py`.
- Die Lernregel steht nur in `network.py`; die Website spielt gespeicherte Stände ab und trainiert nicht selbst.
- `simulation.py` rechnet dieselbe Mathematik wie `network.forward()`, nur neuronweise – beide müssen übereinstimmen. `web/index.html` spiegelt diese Rechnung in JavaScript und prüft sich beim Laden selbst (`forwardCheck` in `data.js`).

## Bauen, Testen, Linten

```bash
~/.local/bin/uv venv --python 3.12 .venv
~/.local/bin/uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m tic_tac_toe.train
.venv/bin/pytest -q
.venv/bin/ruff check . && .venv/bin/ruff format --check .
```

## Projektspezifische Regeln

- UI-Sprache: Deutsch
- Ordnername bleibt `TikTakToe` (Schreibweise von Jonas), das Python-Paket heißt `tic_tac_toe`.
- Ordner: `VS Code/Insy/Neuronale Netze/TikTakToe` – als eigenen Ordner öffnen.

## Team / Git

- Autor: Jonas Pichler
- Repository `INSY` umfasst den ganzen Ordner `Insy` (auch 7Segment); Git-Befehle wirken auf alle Projekte darin.
- Branches: `feat/…`, `fix/…`, `docs/…`; nie direkt auf `main` (Ausnahme war der erste Commit).
- Commit-Präfix: Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- `models/model.json` und `web/data.js` sind generiert, werden aber mit eingecheckt, damit die Website ohne Training läuft.
