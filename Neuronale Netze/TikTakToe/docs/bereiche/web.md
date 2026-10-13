# Bereich: web

## Zweck

Oberfläche des Projekts: gegen das Netz spielen, Rechnung der Knoten ansehen, Training abspielen. Trainiert nicht selbst.

## Schnittstelle nach außen

Liest `window.MODEL_DATA` aus `web/data.js` (geschrieben von `export_html.export_training()`):

| Feld | Inhalt |
|---|---|
| `snapshots[]` | `epoch`, `loss`, `bestMoveRate`, `network` (Gewichte, auf 4 Stellen gerundet) |
| `forwardCheck` | `inputs`, `outputs` – eine von Python gerechnete Beispielstellung |
| `outcomesAsX`, `outcomesAsO` | `wins`, `draws`, `losses` des fertig trainierten Netzes |
| `learningRate`, `sampleCount`, `winLines` | Anzeige und Spielregeln |

## Aufbau intern

Eine Datei `web/index.html` (CSS-Tokens, HTML, JavaScript). Abschnitte im Skript: Spielregeln · Netz-Mathematik · Zustand · Spielfeld · Netzgraph · Trainingszahlen und Diagramme · Aktionen · Start.

## Wichtige Details / Stolperfallen

- `render()` rechnet immer neu: Netz des gewählten Stands, Spielfeld aus Sicht des Spielers am Zug.
- Das Spiel benutzt die Gewichte des gewählten Stands – bei Epoche 0 spielt man gegen das untrainierte Netz.
- Kanten und Knoten werden einmal angelegt (`buildNetwork`), danach nur umgefärbt (`drawNetwork`).
- Kanten-Modus „Änderung“: Wert = Gewicht jetzt − Gewicht im Stand davor. Beim ersten Stand gibt es keine Änderung.
- Dicke/Deckkraft sind bei `WEIGHT_CAP` (8) bzw. `CHANGE_CAP` (0,5) gedeckelt; größere Werte sehen gleich aus.
- Selbsttest beim Laden: weicht die JavaScript-Rechnung von `forwardCheck` ab, erscheint eine Fehlerkarte.
- Spielregeln und Zugwahl sind doppelt vorhanden (Python und JavaScript) und müssen gleich bleiben.

## Tests

Keine automatischen (kein Node im Projekt). Geprüft mit Chrome ohne Fenster und der Prüfliste im Prompt-Protokoll.
