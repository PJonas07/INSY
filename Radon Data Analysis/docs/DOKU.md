# Radon Data Analysis – Dokumentation

Kategorie: <offen – noch nicht geklärt> · Team: <offen> · Stand: 2026-10-13

<!-- Wird automatisch von ~/Programming/Claude/scripts/token_stats.py gefüllt (Stop-Hook). Nicht von Hand bearbeiten. -->
<!-- TOKENS:START -->
## Tokenverbrauch

_Automatisch aktualisiert · Stand 2026-10-13 16:40 · 1 Sitzung(en) · 7 Prompts · 47 Anfragen an das Modell_

| Kennzahl | Tokens | Kosten | Bedeutung |
|---|---:|---:|---|
| **Aktueller Kontext** | 289.051 | – | So viel Text liest Claude derzeit pro Anfrage (Verlauf + Regeln + Dateien) |
| **Neu gelesen** | 217.024 | $ 1,74 | Text, der zum ersten Mal verarbeitet wurde (Prompts, Dateien, Befehlsausgaben) |
| **Geschrieben** | 105.901 | $ 2,12 | Antworten, Code und Denken von Claude |
| Wiederholt gelesen (Cache) | 8.190.689 | $ 1,64 | Bisheriger Verlauf, bei jeder Anfrage erneut gelesen – sehr günstig (5–10 % des Input-Preises) |
| **Gesamt** | 8.513.614 | **$ 5,49** | Token-Summe wird vom Cache dominiert, die Kosten nicht |

_Kosten = API-Listenpreise laut `scripts/prices.json`. Mit einem Claude-Abo (Pro/Max) wird nicht pro Token abgerechnet – dann zeigt der Wert, was die Nutzung über die API kosten würde._

### Pro Prompt (letzte 7 von 7)

| Zeit | Prompt | Anfragen | Neu gelesen | Geschrieben | Cache | Kontext danach |
|---|---|---:|---:|---:|---:|---:|
| 10-13 16:06 | Neues Projekt: Les dir das Daten set von Rad… | 11 | 43,5 k | 13,0 k | 546,3 k | 68,9 k |
| 10-13 16:16 | Präsentiere mir das schön in einer htlm webs… | 15 | 89,0 k | 46,5 k | 2,34 Mio. | 204,6 k |
| 10-13 16:27 | Schreibe Generell dazu. Woher kommt der Refe… | 9 | 57,2 k | 29,3 k | 2,02 Mio. | 261,7 k |
| 10-13 16:33 | Was kann man gegen Radon im haus machen. Ver… | 3 | 6,9 k | 3,3 k | 794,0 k | 268,6 k |
| 10-13 16:35 | Was sind die Daten, die die einzelnen Räume… | 3 | 5,5 k | 4,1 k | 812,4 k | 274,1 k |
| 10-13 16:38 | Gleicher Kontent aber kompakter | 2 | 2,6 k | 1,3 k | 550,2 k | 276,7 k |
| 10-13 16:39 | in der website | 4 | 12,4 k | 8,3 k | 1,12 Mio. | 289,1 k |
<!-- TOKENS:END -->

<!-- Dauerhafte Doku. Beschreibt den aktuellen Zustand, wird nach jeder Änderung aktualisiert. Verlauf steht in ~/Programming/Doku/. -->

## Zweck

<offen – Ziel, Zielgruppe und Abgabetermin noch nicht geklärt>

## Aktueller Stand

- **Fertig:** Datensatz gesichtet (Struktur, Zeitraum, Auffälligkeiten, Abwesenheiten, Raum-Rangliste, Lüftung – siehe unten).
- **Fertig:** Website mit Diagrammen (`website/index.html`), Daten dafür aus `scripts/build_site_data.py`, 17 Tests. Linien lassen sich über die Legende aus- und einblenden. Tabelle „Raum für Raum“ (Tagesgang, höchster Monat, Stunden über 100) aus `roomProfiles`.
- **Fertig:** Hintergrund zu Radon (Wirkung, Halbwertszeit, Referenzwert, Ländervergleich, Hotspots, Bauweise) auf der Website und im Bericht, mit Quellen.
- **In Arbeit:** –
- **Als Nächstes:** Kategorie und Ziel klären, danach Plan für die Analyse.

## Karte

| Bereich | Zweck | Dateien / Ordner | Schnittstelle nach außen | Detail-Doku | Hängt ab von |
|---|---|---|---|---|---|
| Dataset | Rohdaten der Radon-, Raumluft- und Wettermessung | `Dataset/radon_sample_data.csv` | CSV, 29 Spalten, Zeitstempel in Spalte 1 (UTC) und 2 (Europe/Vienna) | – | – |
| Ergebnisse | Ausführlicher Bericht der ersten Datensichtung | `docs/ergebnisse-sichtung.md` | Markdown-Bericht | – | Dataset |
| Datenaufbereitung | Rechnet alle Kennzahlen und Diagrammdaten aus der CSV | `scripts/build_site_data.py`, `tests/` | schreibt `website/data.js` (`window.RADON_DATA`) | – | Dataset |
| Website | Zeigt die Ergebnisse mit Diagrammen, rechnet selbst nichts | `website/index.html`, `styles.css`, `app.js`, `data.js` (generiert) | im Browser öffnen | – | Datenaufbereitung |

Ablauf: CSV → `build_site_data.py` → `data.js` → `app.js` zeichnet die Diagramme als SVG.

## Datensatz

- 229 403 Zeilen, 29 Spalten, 19,8 MB, Zeitraum 2026-03-24 bis 2026-10-13, zeitlich sortiert, keine Duplikate.
- **Langes Format in breiter Tabelle:** Jede Zeile ist die Meldung *eines* Geräts, alle anderen Spalten sind leer. Vor jeder Auswertung auf ein gemeinsames Zeitraster bringen (z. B. Stundenmittel).
- Messintervall: Radon ca. 10 min, Raumluft (Küche, Schlafzimmer) 10 min, Wetter 60 min.
- Geräte starten zu unterschiedlichen Zeiten (Küche 24.03., Büro/Wohnzimmer 27.03., Sockel 30.03., Technikraum/Werkstatt 01.04., Raumluft Küche 08.05., Schlafzimmer 13.05., Luftfeuchte erst ab 10.07.).

## Erkenntnisse aus der Sichtung

Alle Werte aus Stundenmitteln, 0-Werte direkt nach einem Geräte-Neustart entfernt. Vermutungen sind als solche markiert.

- **Urlaub:** Fr 31.07. ca. 05–07 Uhr bis Do 06.08. 20:03 Uhr. Erkennbar an CO₂ (kein Anstieg mehr, Abfall auf ca. 410 ppm). Radon steigt in dieser Zeit in allen Räumen auf 260–360 Bq/m³ (Mittel) und fällt nach der Rückkehr binnen ca. 1,5 h auf unter 25.
- **Zweite Abwesenheit:** Mo 20.07. ca. 07–24 Uhr, gleiches Muster (Radon bis 250–500 Bq/m³).
- **Vermutung:** In beiden Fällen war die Wohnraumlüftung aus oder gedrosselt – bei laufender Überdrucklüftung dürfte Radon in einem leeren Haus nicht steigen. Nicht belegt, beim Hausbesitzer nachfragen.
- **Lüftungseinbau, Vermutung:** 30./31.03.2026. Küche davor im Mittel 204 Bq/m³ (24.–30.03.), danach 42 (April). Davor gibt es nur 6 Tage Daten von 1–3 Sensoren.
- **Überdruck ist in den Daten nicht messbar:** Die Differenz Innen- zu Wetterdruck schwankt um ±0,5 hPa, ein Lüftungsüberdruck läge bei wenigen Pa.
- **Raum-Rangliste im Normalbetrieb** (gemeinsamer Zeitraum ab 13.05., ohne Urlaub, Mittel in Bq/m³): Werkstatt 60, Technikraum 56, Küche-Sockel 53, Schlafzimmer 43, Wohnzimmer 32, Küche 29, Büro 28.
- **Rangliste im Urlaub:** Küche-Sockel 355, Schlafzimmer 347, Küche 296, Wohnzimmer 296, Werkstatt 284, Technikraum 267, Büro 256.
- **Technikraum und Werkstatt** verhalten sich anders als die Wohnräume: 09.–21.08. bei 150–250 Bq/m³, während die Wohnräume bei ca. 30 liegen.
- **CO₂ gibt es erst ab 08.05.** – Abwesenheiten davor sind nicht erkennbar.

## Bedienung

```bash
~/.local/bin/python3.12 scripts/build_site_data.py        # website/data.js neu erzeugen
~/.local/bin/python3.12 -m unittest discover tests       # Tests
open website/index.html                                   # Website ansehen
```

Keine Abhängigkeiten: nur Python-Standardbibliothek, im Browser kein Framework und keine Diagramm-Bibliothek.

## Wichtige Entscheidungen

| Datum | Entscheidung | Grund |
|---|---|---|
| 2026-10-13 | Diagramme als handgeschriebenes SVG, keine Bibliothek | Keine Dependency ohne Rücksprache; jede Zeile erklärbar |
| 2026-10-13 | Daten als `data.js` statt JSON | Seite läuft per Doppelklick (`file://`), dort blockiert der Browser `fetch()` |
| 2026-10-13 | Alle Berechnungen in Python, JavaScript zeichnet nur | Rechnung an einer Stelle, mit Tests prüfbar |
| 2026-10-13 | Referenzwerte der Länder als Konstante in `app.js`, nicht in `data.js` | Literaturwerte, keine Messdaten; `data.js` bleibt rein aus der CSV erzeugt |
| 2026-10-13 | Website nur lokal, nicht veröffentlicht | Daten zeigen, wann ein Privathaus leer stand |

## Bekannte Probleme / Einschränkungen

- **0-Werte nach Neustart:** Fällt die Betriebszeit auf 0, meldet das Gerät zunächst 0 Bq/m³. Das sind Artefakte, keine Messwerte.
- **Viele 0-Werte in Technikraum/Werkstatt** von April bis Juni (ca. 570 bzw. 710), auch ohne Neustart – unklar, ob echt.
- **Betriebszeit-Zähler** springt gelegentlich um genau 31 min zurück.
- **Schlafzimmer** ist ein anderer Sensortyp („RQ“ laut Jonas; Nachkommastellen, keine Betriebszeit) – nicht 1:1 mit den anderen Radonsensoren vergleichbar.
- **Lücke** Technikraum/Werkstatt 11.–13.06. (38,7 h); Wetterdaten mit Lücken bis 14 h.
