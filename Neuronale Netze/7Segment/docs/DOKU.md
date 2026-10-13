# 7Segment – Dokumentation

Kategorie: Schule · Team: allein (Jonas) · Stand: 2026-10-13

<!-- Wird automatisch von ~/Programming/Claude/scripts/token_stats.py gefüllt (Stop-Hook). Nicht von Hand bearbeiten. -->
<!-- TOKENS:START -->
## Tokenverbrauch

_Automatisch aktualisiert · Stand 2026-10-13 15:45 · 3 Sitzung(en) · 4 Prompts · 21 Anfragen an das Modell_

| Kennzahl | Tokens | Kosten | Bedeutung |
|---|---:|---:|---|
| **Aktueller Kontext** | 186.412 | – | So viel Text liest Claude derzeit pro Anfrage (Verlauf + Regeln + Dateien) |
| **Neu gelesen** | 57.950 | $ 0,46 | Text, der zum ersten Mal verarbeitet wurde (Prompts, Dateien, Befehlsausgaben) |
| **Geschrieben** | 23.747 | $ 0,47 | Antworten, Code und Denken von Claude |
| Wiederholt gelesen (Cache) | 2.744.023 | $ 0,55 | Bisheriger Verlauf, bei jeder Anfrage erneut gelesen – sehr günstig (5–10 % des Input-Preises) |
| **Gesamt** | 2.825.720 | **$ 1,49** | Token-Summe wird vom Cache dominiert, die Kosten nicht |

_Kosten = API-Listenpreise laut `scripts/prices.json`. Mit einem Claude-Abo (Pro/Max) wird nicht pro Token abgerechnet – dann zeigt der Wert, was die Nutzung über die API kosten würde._

### Pro Prompt (letzte 4 von 4)

| Zeit | Prompt | Anfragen | Neu gelesen | Geschrieben | Cache | Kontext danach |
|---|---|---:|---:|---:|---:|---:|
| 09-29 20:39 | Bitte überarbeite das alles | 10 | 17,2 k | 13,8 k | 1,72 Mio. | 180,5 k |
| 10-13 15:20 | Bitte mache das TikTakToe Projekt wie das 7S… | 7 | 36,4 k | 6,2 k | 290,4 k | 57,9 k |
| 10-13 15:43 | Mache so eine kurz Doku auch für 7 Segment | 3 | 3,7 k | 3,3 k | 548,2 k | 185,7 k |
| 10-13 15:45 | Wo sind die Trainingsdaten | 1 | 719 | 472 | 185,7 k | 186,4 k |
<!-- TOKENS:END -->

## Zweck

Lernprojekt „Neuronale Netze“: Ein selbst programmiertes Netz erkennt Ziffern auf einer 7-Segment-Anzeige. Visualisierungen zeigen, wie jeder Knoten berechnet wird.

## Aktueller Stand

- **Fertig:** Netz (NumPy, Backpropagation), Konsolen-Training, Tests (20), Desktop-App mit Schritt-Simulation und Live-Training, HTML-Visualisierung.
- **Kurzfassung:** `docs/KURZDOKU.md` (was gemacht wurde, wie umgesetzt).
- **In Arbeit:** –
- **Als Nächstes:** Code durchgehen; optional Experimente (andere Hidden-Größe, Lernrate).

## Karte

| Bereich | Zweck | Dateien / Ordner | Schnittstelle nach außen | Detail-Doku | Hängt ab von |
|---|---|---|---|---|---|
| config | Hyperparameter, Pfade | `seven_segment/config.py` | Konstanten | – | – |
| dataset | Trainingsdaten | `seven_segment/dataset.py` | `load_inputs()`, `load_targets()`, `segments_for_digit()`, `SEGMENT_NAMES` | – | – |
| network | Netz + Training | `seven_segment/network.py` | `NeuralNetwork.forward/train_step/train/predict/save/load`, `sigmoid` | `docs/bereiche/network.md` | config |
| simulation | Knoten-für-Knoten-Rechnung | `seven_segment/simulation.py` | `compute_steps(network, segments) -> list[NodeStep]`, `NodeStep.formula()` | `docs/bereiche/network.md` | network |
| train / export | Training, Speichern, Export fürs Web | `seven_segment/train.py`, `export_html.py` | CLI, `export_model()` | – | network, dataset |
| gui | Desktop-App | `seven_segment/gui.py` | `python -m seven_segment.gui` | – | alle oben |
| web | HTML-Visualisierung | `web/index.html`, `web/data.js` (generiert) | `window.MODEL_DATA` | – | export |

Datenfluss: `train.py` → `models/model.json` + `web/data.js` → `gui.py` lädt model.json, `index.html` lädt data.js.

## Bedienung

Siehe `README.md` (Setup, Training, GUI, HTML, Tests).

## Wichtige Entscheidungen

| Datum | Entscheidung | Grund |
|---|---|---|
| 2026-09-29 | Netz selbst mit NumPy (ADR-0001) | erklärbar, kleine Dependency |
| 2026-09-29 | 7 → 8 → 10, Sigmoid, lr 2.0, 3000 Epochen, Seed 42 | lernt alle Ziffern sicher (> 0.9) in < 1 s |
| 2026-09-29 | Flaches Paket `seven_segment/` statt `src/`-Layout | `python -m` direkt aus dem Projektordner, ohne Installation |
| 2026-09-29 | `data.js` statt `data.json` | Browser blockieren `fetch()` bei `file://` |
| 2026-09-29 | Python 3.12 per `uv` im Benutzerordner installiert | System hatte nur 3.9 |
| 2026-09-29 | Projekt nach `VS Code/Insy/` verschoben, `.venv` neu angelegt | Einordnung ins Fach Insy; venv enthält absolute Pfade |
| 2026-09-29 | Token-Hook nicht mehr pro Projekt (global) | `.claude/settings.json` enthält nur noch Berechtigungen |

## Bekannte Probleme / Einschränkungen

- Dunkelmodus-Erkennung der GUI nutzt einen internen Tk-Befehl (macOS); sonst hell. Markiert mit `VERIFY`.
- GUI-Layout nicht automatisch per Screenshot geprüft (Terminal ohne Bildschirmaufnahme-Recht).
- Ungültige Muster (z. B. nur Segment a) liefern trotzdem eine Ziffer – das Netz kennt keine Klasse „keine Ziffer“.
