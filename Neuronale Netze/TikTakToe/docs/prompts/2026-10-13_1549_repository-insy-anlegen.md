# Repository INSY anlegen

**Datum:** 2026-10-13 15:49

## Prompt

> Erstelle ein neues Repository INSY und Lade alles was auch in INSY Ordner lokal ist hoch

## Was gemacht wurde

- Ordner `Insy` geprüft: zwei Projekte (7Segment, TikTakToe), keine Secrets, keine großen Dateien.
- Git-Repository im Ordner `Insy` angelegt (`main`), `.gitignore` aus der Vorlage (ohne `.venv`, Caches, `.DS_Store`).
- Das leere Repository in `TikTakToe` (kein Commit) entfernt, damit es nicht als Repository im Repository landet.
- Erster Commit mit beiden Projekten.
- `CLAUDE.md` beider Projekte und `docs/DOKU.md` (TikTakToe) an das gemeinsame Repository angepasst.
- **Nicht hochgeladen:** GitHub CLI ist nicht angemeldet (`gh auth login` fehlt).

## Geänderte Dateien

- `Insy/.gitignore` – neu
- `TikTakToe/CLAUDE.md`, `TikTakToe/docs/DOKU.md`, `7Segment/CLAUDE.md` – geändert

## Offen

- Jonas: `gh auth login` ausführen, danach Repository auf GitHub anlegen und pushen.
- Sichtbarkeit: Vorschlag privat.
