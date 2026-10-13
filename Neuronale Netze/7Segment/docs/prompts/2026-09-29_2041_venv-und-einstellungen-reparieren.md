# venv und Einstellungen reparieren

**Datum:** 2026-09-29 20:41

## Prompt

> Bitte überarbeite das alles

(Überarbeitung der Regeln im Claude-Ordner; betrifft dieses Projekt nach dem Verschieben nach `VS Code/Insy/`.)

## Was gemacht wurde

- `.venv` neu angelegt (alte Pfade zeigten auf den früheren Ordner), `requirements.txt` installiert.
- 20 Tests grün, ruff sauber, Modell neu trainiert und exportiert (identisch, fester Seed).
- `CLAUDE.md`: `Git: nein`, neuer Ordnerpfad.
- `.claude/settings.json`: Token-Hook entfernt (läuft jetzt global), Freigaben für `.venv/bin/…`.
- `docs/DOKU.md`: Entscheidungen ergänzt.

## Geänderte Dateien

- `.venv/` – neu angelegt
- `CLAUDE.md`, `docs/DOKU.md`, `.claude/settings.json` – geändert
- `models/model.json`, `web/data.js` – neu erzeugt

## Offen

- Projekt künftig direkt als Ordner öffnen, damit der Token-Block gefüllt wird.
