# Bereich: minimax + dataset

## Zweck

Legt fest, was das Netz lernen soll: zu jeder Stellung die besten Züge. Kennt das Netz nicht.

## Schnittstelle nach außen

- `best_moves(board, player) -> list[int]` – alle Felder mit der höchsten Bewertung.
- `score_move(board, cell, player) -> int`, `score_position(board, player) -> int`.
- `load_dataset() -> (inputs, targets)` – zwei Matrizen (4520, 9).
- `encode_board(board, player) -> list[int]`, `collect_positions()`.

## Aufbau intern

| Datei | Inhalt |
|---|---|
| `tic_tac_toe/minimax.py` | rekursive Suche mit Merkliste (`_score_cache`) |
| `tic_tac_toe/dataset.py` | alle Stellungen sammeln, kodieren, Ziele setzen |

## Wichtige Details / Stolperfallen

- Bewertung immer aus Sicht des Spielers am Zug: Sieg positiv, Remis 0, Niederlage negativ.
- `score_move` zieht die Bewertung des Gegners mit Minus heran („gut für ihn = schlecht für mich“) und schiebt sie einen Schritt Richtung 0. Dadurch ist ein Sieg in 1 Zug (9) mehr wert als ein Sieg in 3 Zügen (7).
- Eine beendete Stellung mit Sieger bedeutet immer: Der Spieler am Zug hat verloren (der letzte Zug kam vom Gegner).
- Eingabe = `board * player`: eigene Steine 1, gegnerische −1. X und O teilen sich so ein Netz.
- Ziel hat oft mehrere Einsen (im Schnitt 1,58); beim leeren Feld sind alle 9 Züge gleich gut.
- Stellungen werden sortiert, damit das Training bei jedem Lauf gleich abläuft.

## Tests

`tests/test_minimax.py`, `tests/test_dataset.py` – `.venv/bin/pytest -q`
