# TikTakToe – Dokumentation

Kategorie: Schule · Team: allein (Jonas) · Stand: 2026-10-13

<!-- Wird automatisch von ~/Programming/Claude/scripts/token_stats.py gefüllt (Stop-Hook). Nicht von Hand bearbeiten. -->
<!-- TOKENS:START -->
## Tokenverbrauch

_Automatisch aktualisiert · Stand 2026-10-13 15:45 · 1 Sitzung(en) · 3 Prompts · 32 Anfragen an das Modell_

| Kennzahl | Tokens | Kosten | Bedeutung |
|---|---:|---:|---|
| **Aktueller Kontext** | 182.027 | – | So viel Text liest Claude derzeit pro Anfrage (Verlauf + Regeln + Dateien) |
| **Neu gelesen** | 160.499 | $ 1,28 | Text, der zum ersten Mal verarbeitet wurde (Prompts, Dateien, Befehlsausgaben) |
| **Geschrieben** | 77.471 | $ 1,55 | Antworten, Code und Denken von Claude |
| Wiederholt gelesen (Cache) | 3.629.162 | $ 0,73 | Bisheriger Verlauf, bei jeder Anfrage erneut gelesen – sehr günstig (5–10 % des Input-Preises) |
| **Gesamt** | 3.867.132 | **$ 3,56** | Token-Summe wird vom Cache dominiert, die Kosten nicht |

_Kosten = API-Listenpreise laut `scripts/prices.json`. Mit einem Claude-Abo (Pro/Max) wird nicht pro Token abgerechnet – dann zeigt der Wert, was die Nutzung über die API kosten würde._

### Pro Prompt (letzte 3 von 3)

| Zeit | Prompt | Anfragen | Neu gelesen | Geschrieben | Cache | Kontext danach |
|---|---|---:|---:|---:|---:|---:|
| 10-13 15:24 | Nimm den ordern TikTakToe und setze es wie 7… | 12 | 82,2 k | 20,0 k | 862,9 k | 103,8 k |
| 10-13 15:31 | Mit Git; Führe das Projekt aus und es ist no… | 18 | 74,2 k | 54,3 k | 2,41 Mio. | 177,9 k |
| 10-13 15:42 | Alles Getestet. Funktioniert perfekt. Mache… | 2 | 4,1 k | 3,2 k | 357,3 k | 182,0 k |
<!-- TOKENS:END -->

## Zweck

Lernprojekt „Neuronale Netze“: Ein selbst programmiertes Netz lernt Tic-Tac-Toe von einem perfekten Lehrer (Minimax). Eine Website zeigt das Spiel, die Rechnung jedes Knotens und wie sich die Gewichte beim Training ändern.

## Aktueller Stand

- **Fertig:** Spielregeln, Minimax, Datensatz (4520 Stellungen), Netz 9 → 36 → 9 (NumPy, Backpropagation), Training mit 51 Gewichts-Ständen, Bewertung der Spielstärke, Konsolenspiel, Website, 62 Tests, ruff sauber.
- **Ergebnis (Seed 42):** 97,1 % beste Züge; als X 72 Siege / 4 Remis / 0 Niederlagen, als O 344 / 132 / 21.
- **Von Jonas geprüft (2026-10-13):** Website nach Prüfliste, „funktioniert“.
- **Kurzfassung:** `docs/KURZDOKU.md` (was gemacht wurde, wie umgesetzt).
- **In Arbeit:** –
- **Git:** erster Commit im Repository `INSY` (lokal). Hochladen zu GitHub wartet auf `gh auth login`.
- **Als Nächstes:** Code durchgehen.

## Karte

| Bereich | Zweck | Dateien / Ordner | Schnittstelle nach außen | Detail-Doku | Hängt ab von |
|---|---|---|---|---|---|
| config | Hyperparameter, Pfade | `tic_tac_toe/config.py` | Konstanten | – | – |
| game | Spielregeln | `tic_tac_toe/game.py` | `new_board()`, `find_winner()`, `legal_moves()`, `is_game_over()`, `apply_move()`, `format_board()`, `PLAYER_X/O`, `EMPTY`, `WIN_LINES` | – | – |
| minimax | perfekter Lehrer | `tic_tac_toe/minimax.py` | `best_moves(board, player)`, `score_move()`, `score_position()` | `docs/bereiche/lehrer-und-daten.md` | game |
| dataset | Trainingsdaten | `tic_tac_toe/dataset.py` | `load_dataset() -> (inputs, targets)`, `encode_board()`, `collect_positions()` | `docs/bereiche/lehrer-und-daten.md` | game, minimax |
| network | Netz + Lernregel | `tic_tac_toe/network.py` | `NeuralNetwork.forward/compute_gradients/train_step/train/save/load`, `sigmoid` | `docs/bereiche/network.md` | config |
| simulation | Knoten-für-Knoten-Rechnung | `tic_tac_toe/simulation.py` | `compute_steps(network, inputs) -> list[NodeStep]`, `NodeStep.formula()` | `docs/bereiche/network.md` | network |
| evaluation | Zug wählen, Spielstärke messen | `tic_tac_toe/evaluation.py` | `choose_move()`, `best_move_rate()`, `count_outcomes() -> Outcomes` | – | network, dataset, game |
| training | Trainingsschleife mit Ständen | `tic_tac_toe/training.py` | `train_with_snapshots() -> list[Snapshot]` | `docs/bereiche/network.md` | network, evaluation |
| train / export | Konsole: trainieren, speichern, Web-Daten | `tic_tac_toe/train.py`, `export_html.py` | `python -m tic_tac_toe.train`, `export_training()` | – | training, evaluation |
| play | Konsolenspiel | `tic_tac_toe/play.py` | `python -m tic_tac_toe.play` | – | evaluation, game |
| web | Website | `web/index.html`, `web/data.js` (generiert) | `window.MODEL_DATA` | `docs/bereiche/web.md` | export |

Datenfluss: `minimax` → `dataset` → `training` (Netz lernt, Stände werden gemerkt) → `train.py` schreibt `models/model.json` (Endgewichte) und `web/data.js` (alle Stände) → `play.py` lädt model.json, `index.html` lädt data.js.

## Bedienung

Siehe `README.md` (Setup, Training, Konsolenspiel, Website, Tests).

## Wichtige Entscheidungen

| Datum | Entscheidung | Grund |
|---|---|---|
| 2026-10-13 | Aufbau, Dependencies und Stil wie 7Segment | Auftrag „wie 7Segment“ |
| 2026-10-13 | Netz lernt überwacht von Minimax, kein Reinforcement Learning (ADR-0001) | gleiche Mathematik wie 7Segment, erklärbar |
| 2026-10-13 | Eingabe aus Sicht des Spielers am Zug (1 / −1 / 0) | ein Netz für X und O |
| 2026-10-13 | Ziel = alle besten Züge (mehrere Einsen) | oft sind mehrere Züge gleich gut |
| 2026-10-13 | 9 → 36 → 9, Lernrate 10, 5000 Epochen, Seed 42 | Probeläufe: 97 % beste Züge in ca. 6 s, Graph noch lesbar |
| 2026-10-13 | Website spielt in Python gespeicherte Stände ab, trainiert nicht selbst | Lernregel existiert nur einmal (Python) |
| 2026-10-13 | Selbsttest in der Website (`forwardCheck`) | prüft, dass JavaScript wie Python rechnet |
| 2026-10-13 | Keine tkinter-App | Oberfläche ist laut Auftrag die Website |
| 2026-10-13 | Ein gemeinsames Repository `INSY` für den ganzen Ordner `Insy` statt eines eigenen pro Projekt | Wunsch von Jonas; das leere Projekt-Repository wurde dafür entfernt |

Die Entscheidungen 2–8 hat Claude vorgeschlagen und umgesetzt; Jonas hat nach der Rückfrage nur „mit Git“ und „Website fehlt“ geantwortet.

## Bekannte Probleme / Einschränkungen

- Das Netz spielt nicht perfekt: Als zweiter Spieler (O) verliert es 21 von 497 möglichen Spielverläufen. Größere Netze waren in den Probeläufen besser (45 Hidden: 11 Niederlagen), aber keines unschlagbar.
- Hidden-Knoten im Graph sind klein; für Tastatur und Touch gibt es deshalb die Auswahlliste „Rechnung eines Knotens“.
- Die Sitzung lief aus `~/Programming` statt aus dem Projektordner: Tokenzahlen werden nur näherungsweise zugeordnet.
