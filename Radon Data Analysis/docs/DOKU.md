# Radon Data Analysis – Dokumentation

Kategorie: Schule · Team: <offen> · Stand: 2026-11-17

<!-- Wird automatisch von ~/Programming/Claude/scripts/token_stats.py gefüllt (Stop-Hook). Nicht von Hand bearbeiten. -->
<!-- TOKENS:START -->
## Tokenverbrauch

_Automatisch aktualisiert · Stand 2026-11-17 16:29 · 11 Sitzung(en) · 19 Prompts · 202 Anfragen an das Modell_

| Kennzahl | Tokens | Kosten | Bedeutung |
|---|---:|---:|---|
| **Aktueller Kontext** | 36.102 | – | So viel Text liest Claude derzeit pro Anfrage (Verlauf + Regeln + Dateien) |
| **Neu gelesen** | 691.602 | $ 2,70 | Text, der zum ersten Mal verarbeitet wurde (Prompts, Dateien, Befehlsausgaben) |
| **Geschrieben** | 224.483 | $ 3,18 | Antworten, Code und Denken von Claude |
| Wiederholt gelesen (Cache) | 29.383.593 | $ 5,68 | Bisheriger Verlauf, bei jeder Anfrage erneut gelesen – sehr günstig (5–10 % des Input-Preises) |
| **Gesamt** | 30.299.678 | **$ 11,56** | Token-Summe wird vom Cache dominiert, die Kosten nicht |

_Kosten = API-Listenpreise laut `scripts/prices.json`. Mit einem Claude-Abo (Pro/Max) wird nicht pro Token abgerechnet – dann zeigt der Wert, was die Nutzung über die API kosten würde._
_Achtung: keine Preise für claude-haiku-5-5 – in `prices.json` ergänzen, sonst sind die Kosten zu niedrig._

### Pro Prompt (letzte 10 von 19)

| Zeit | Prompt | Anfragen | Neu gelesen | Geschrieben | Cache | Kontext danach |
|---|---|---:|---:|---:|---:|---:|
| 11-17 16:09 | Website aktualisieren und zusätzlich eine We… | 26 | 69,8 k | 24,9 k | 6,53 Mio. | 282,4 k |
| 11-17 16:10 | From the WHO Handbook on Indoor Radon (2009)… | 3 | 36,0 k | 2,3 k | 10,6 k | 36,0 k |
| 11-17 16:10 | Fetch https://www.unscear.org/unscear/upload… | 2 | 2,5 k | 622 | 7,1 k | 5,4 k |
| 11-17 16:10 | I need national average indoor (residential)… | 3 | 111,7 k | 5,9 k | 89,5 k | 114,5 k |
| 11-17 16:15 | Project path: /Users/jonas/Programming/VS Co… | 8 | 34,8 k | 9,1 k | 180,4 k | 34,8 k |
| 11-17 16:20 | Länder einzeichnen. Kondensator formel wegma… | 17 | 46,2 k | 24,9 k | 5,23 Mio. | 330,0 k |
| 11-17 16:24 | Project path: /Users/jonas/Programming/VS Co… | 5 | 30,9 k | 8,8 k | 88,8 k | 30,9 k |
| 11-17 16:24 | commiten und pushen | 3 | 3,5 k | 1,4 k | 995,3 k | 334,5 k |
| 11-17 16:25 | PR nach main anlegen; Mache dann eine Einsch… | 17 | 27,9 k | 18,3 k | 5,93 Mio. | 362,4 k |
| 11-17 16:29 | Project path: /Users/jonas/Programming/VS Co… | 7 | 32,0 k | 10,8 k | 152,3 k | 36,1 k |
<!-- TOKENS:END -->

<!-- Dauerhafte Doku. Beschreibt den aktuellen Zustand, wird nach jeder Änderung aktualisiert. Verlauf steht in ~/Programming/Doku/. -->

## Zweck

<offen – Ziel, Zielgruppe und Abgabetermin noch nicht geklärt>

## Aktueller Stand

- **Fertig:** Datensatz gesichtet (Struktur, Zeitraum, Auffälligkeiten, Abwesenheiten, Raum-Rangliste, Lüftung – siehe unten).
- **Fertig:** Website mit Diagrammen (`website/index.html`), Daten dafür aus `scripts/build_site_data.py`, 30 Tests (alle Tests in `tests/`). Linien lassen sich über die Legende aus- und einblenden. Tabelle „Raum für Raum“ (Tagesgang, höchster Monat, Stunden über 100) aus `roomProfiles`.
- **Fertig:** Wohnraumlüftung (ab 24.08.2026) mit Vorher-/Nachher-Vergleich in Daten und Website; Marker „Lüftung an“ und „Fenster gekippt“ im Übersichtsdiagramm.
- **Fertig:** Einschätzung ganz oben auf der Website („Ist Radon ein reales Problem?“): allgemein „Ja, aber ein gut beherrschbares.“ in drei Spalten (Warum ja / Warum beherrschbar / Und dieses Haus?). Der Hausbezug ist ein Satz, gefüllt aus Hauszahlen in `data.js`.
- **Fertig:** Radon-Hintergrund auf der Website („Radon allgemein“): Risiko 100 gegen 1 000 Bq/m³, Lunge und Kinder, österreichische Grenzwerte als Zeitstrahl 1990–2020, Zerfallstabelle eingeklappt (`<details>`), zweispaltige Layouts. Quellen klein (11 px) direkt unter jedem Abschnitt. Im Bericht unter Abschnitt 9.
- **Fertig:** Weltkugel „Radon auf der ganzen Welt“ im Radon-Hintergrund: Länder als gefüllte Umrisse (177 Länder aus Natural Earth 1:110m, `world.js`), in vier Klassen eingefärbt, Länder ohne Wert grau. Weltmittel 39 Bq/m³, Drehen per Ziehen oder Pfeiltasten, Drehung hält beim Fokus an und entfällt bei „Bewegung reduzieren“, Markierung „Dieses Haus“. Klassen aus Karten abgelesen (siehe Probleme).
- **Fertig:** Dichte des Hauses per Kondensator-Modell (Abschnitt „Wie dicht ist das Haus?“): Abklingzeit im Urlaub, Eintrag von außen, Winter-Schätzung mit und ohne Lüftung. Auf der Website nur die Ergebnisse, Formel und Analogietabelle stehen im Bericht unter Abschnitt 5. Modell in `build_site_data.py`, Daten `houseModel` in `data.js`.
- **In Arbeit:** –
- **Als Nächstes:** Ziel und Abgabetermin klären, danach Plan für die Analyse.

## Karte

| Bereich | Zweck | Dateien / Ordner | Schnittstelle nach außen | Detail-Doku | Hängt ab von |
|---|---|---|---|---|---|
| Dataset | Rohdaten der Radon-, Raumluft- und Wettermessung; Ländergrenzen für die Weltkugel | `Dataset/radon_sample_data.csv`, `Dataset/countries-110m.json` (TopoJSON, Natural Earth 1:110m über npm `world-atlas` 2.0.2, gemeinfrei) | CSV, 29 Spalten, Zeitstempel in Spalte 1 (UTC) und 2 (Europe/Vienna); TopoJSON | – | – |
| Ergebnisse | Ausführlicher Bericht der ersten Datensichtung | `docs/ergebnisse-sichtung.md` | Markdown-Bericht | – | Dataset |
| Datenaufbereitung | Rechnet alle Kennzahlen (inkl. Lüftungsvergleich, Kondensator-Modell der Hausdichte) und Diagrammdaten aus der CSV; wandelt die Ländergrenzen in Koordinaten um | `scripts/build_site_data.py`, `scripts/build_world_data.py`, `tests/` | schreibt `website/data.js` (`window.RADON_DATA`, u. a. Schlüssel `houseModel`) und `website/world.js` (`window.WORLD_COUNTRIES`, ca. 140 KB) | – | Dataset |
| Website | Zeigt die Ergebnisse mit Diagrammen (Einschätzung ganz oben, Radon-Hintergrund mit Weltkugel, Lüftungs- und Dichteabschnitt), rechnet selbst nichts außer der Projektion der Weltkugel | `website/index.html`, `styles.css`, `app.js`, `data.js` (generiert), `world.js` (generiert) | im Browser öffnen | – | Datenaufbereitung |

Ablauf: CSV → `build_site_data.py` → `data.js` → `app.js` zeichnet die Diagramme als SVG. Ländergrenzen: `countries-110m.json` → `build_world_data.py` → `world.js` → `app.js` zeichnet die Länder als SVG-Pfade.

## Datensatz

- 229 403 Zeilen, 29 Spalten, 19,8 MB, Zeitraum 2026-03-24 bis 2026-10-13, zeitlich sortiert, keine Duplikate.
- **Langes Format in breiter Tabelle:** Jede Zeile ist die Meldung *eines* Geräts, alle anderen Spalten sind leer. Vor jeder Auswertung auf ein gemeinsames Zeitraster bringen (z. B. Stundenmittel).
- Messintervall: Radon ca. 10 min, Raumluft (Küche, Schlafzimmer) 10 min, Wetter 60 min.
- Geräte starten zu unterschiedlichen Zeiten (Küche 24.03., Büro/Wohnzimmer 27.03., Sockel 30.03., Technikraum/Werkstatt 01.04., Raumluft Küche 08.05., Schlafzimmer 13.05., Luftfeuchte erst ab 10.07.).

## Erkenntnisse aus der Sichtung

Alle Werte aus Stundenmitteln, 0-Werte direkt nach einem Geräte-Neustart entfernt. Vermutungen sind als solche markiert.

- **Urlaub:** Fr 31.07. ca. 05–07 Uhr bis Do 06.08. 20:03 Uhr. Erkennbar an CO₂ (kein Anstieg mehr, Abfall auf ca. 410 ppm). Radon steigt in dieser Zeit in allen Räumen auf 260–360 Bq/m³ (Mittel) und fällt nach der Rückkehr binnen ca. 1,5 h auf unter 25. Liegt vor dem Lüftungseinbau, bei geschlossenen Fenstern.
- **Zweite Abwesenheit:** Mo 20.07. ca. 07–24 Uhr, gleiches Muster (Radon bis 250–500 Bq/m³). Ebenfalls vor dem Lüftungseinbau.
- **Wohnraumlüftung ab 24.08.2026** (laut Hausbesitzer, bestätigt). Vergleich je 14 Tage vor/nach Start: Technikraum + Werkstatt 162 → 18 Bq/m³ (−89 %), Wohnräume 32 → 24 Bq/m³ (−25 %). Zeiträume: 10.–23.08. gegen 24.08.–06.09.
- **Fenster gekippt ab 31.03.2026** (laut Hausbesitzer). Der Abfall im März ist darauf zurückzuführen, nicht auf die Lüftung. Küche: 204 Bq/m³ (24.–30.03.), danach 42 (April). Davor gibt es nur 6 Tage Daten von 1–3 Sensoren.
- **Überdruck ist in den Daten nicht messbar:** Die Differenz Innen- zu Wetterdruck schwankt um ±0,5 hPa, ein Lüftungsüberdruck läge bei wenigen Pa. Die Erklärung „Überdruck hält Radon draußen“ ist die Aussage des Hausbesitzers, nicht durch die Messung belegt.
- **Raum-Rangliste im Normalbetrieb** (gemeinsamer Zeitraum ab 13.05., ohne Urlaub, Mittel in Bq/m³): Werkstatt 60, Technikraum 56, Küche-Sockel 53, Schlafzimmer 43, Wohnzimmer 32, Küche 29, Büro 28.
- **Rangliste im Urlaub:** Küche-Sockel 355, Schlafzimmer 347, Küche 296, Wohnzimmer 296, Werkstatt 284, Technikraum 267, Büro 256.
- **Technikraum und Werkstatt** verhalten sich anders als die Wohnräume: 09.–21.08. bei 150–250 Bq/m³, während die Wohnräume bei ca. 30 liegen.
- **Dichte des Hauses (Kondensator-Modell, Hausvolumen 675 m³ = 270 m² × 2,5 m, laut Hausbesitzer):** Im Urlaub steigt Radon nach einer Exponentialkurve mit Zeitkonstante τ ≈ 40 h auf einen Endwert ≈ 377 Bq/m³. Daraus: Luftwechsel ≈ 0,018/h (Lüftung aus, Fenster zu), Eintrag von außen ≈ 9,5 Bq/(m³·h), also ≈ 6 400 Bq/h für das ganze Haus. Nach der Rückkehr fällt der Wert mit τ ≈ 72 min (≈ 0,8/h), also weit schneller als der Luftwechsel im Urlaub. Ursache offen (Vermutung: Lüften bei der Rückkehr, nicht in den Daten belegt).
- **Winter (Schätzung über Temperatur-Regression seit 24.08., 0 °C außen):** Geschlossenes Haus ≈ 1 060 Bq/m³ im Gleichgewicht, 300 Bq/m³ nach ca. 12 h (Sommer: ca. 60 h). Mit Lüftung im Winter: Wohnräume ca. 54, Technikraum/Werkstatt ca. 94 Bq/m³. Die Winter-Werte sind Extrapolation, nicht gemessen.
- **CO₂ gibt es erst ab 08.05.** – Abwesenheiten davor sind nicht erkennbar.

## Bedienung

```bash
~/.local/bin/python3.12 scripts/build_site_data.py        # website/data.js neu erzeugen
~/.local/bin/python3.12 scripts/build_world_data.py       # website/world.js neu erzeugen (aus Dataset/countries-110m.json)
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
| 2026-11-17 | Lüftungsstart 24.08.2026 laut Hausbesitzer, nicht 30./31.03. (Annahme); Fenster gekippt ab 31.03. | Hausbesitzer hat bestätigt; der März-Abfall war die gekippten Fenster |
| 2026-11-17 | Lüftungswirkung als Vergleich je 14 Tage vor/nach 24.08. | Gleich lange Zeiträume vor und nach dem Start; Urlaub liegt außerhalb; mit Python nachrechenbar |
| 2026-11-17 | Kondensator-Modell (Gitter-Suche + lineare Regression, nur Standardbibliothek) für Hausdichte | Ein Modell mit wenigen Parametern, mit Tests prüfbar; keine Dependency nötig |
| 2026-11-17 | Winter-Schätzung über Temperatur-Regression seit 24.08.; Luftwechsel konstant angenommen → Obergrenze | Im Winter gibt es keine geschlossene Phase zum Messen; Konstanz ist eine bewusste Vereinfachung |
| 2026-11-17 | Hausvolumen 675 m³ laut Hausbesitzer (270 m² × 2,5 m) | Grundfläche und Raumhöhe vom Hausbesitzer, nicht vermessen |
| 2026-11-17 | Weltkugel als handgeschriebenes SVG (orthografische Projektion), ohne Kartenbibliothek | Keine Dependency ohne Rücksprache; jede Zeile erklärbar |
| 2026-11-17 | Ländergrenzen als Datendatei statt Bibliothek: Natural Earth 1:110m über npm `world-atlas` 2.0.2, eigener TopoJSON-Decoder in `build_world_data.py`, Ergebnis `world.js` | Keine Kartenbibliothek als Dependency; Daten gemeinfrei; Umwandlung einmalig und mit Tests prüfbar, Browser lädt nur die fertige Datei |
| 2026-11-17 | Länderwerte als vier Klassen (7–25, 25–50, 50–100, 100–184 Bq/m³) aus den Karten von Zielinski & Chambers 2008 abgelesen, keine exakten Landeswerte; Konstante `COUNTRIES` in `app.js` | Die Quelle liefert Karten, keine Tabelle; Klassen statt Scheingenauigkeit; gleiches Muster wie `REFERENCE_LEVELS` |
| 2026-11-17 | Quellen direkt unter jedem Abschnitt, klein (11 px), statt Sammelliste am Ende | Wunsch von Jonas: Belege stehen neben der Aussage, die sie belegen |
| 2026-11-17 | Einschätzung „Ist Radon ein reales Problem?“ allgemein formuliert; nur der Satz „Und dieses Haus?“ nutzt Hauszahlen aus `data.js` | Die Frage gilt für jedes Haus; der Hausbezug bleibt eine Zeile, damit die Aussage nicht an einem Haus hängt |

## Bekannte Probleme / Einschränkungen

- **0-Werte nach Neustart:** Fällt die Betriebszeit auf 0, meldet das Gerät zunächst 0 Bq/m³. Das sind Artefakte, keine Messwerte.
- **Viele 0-Werte in Technikraum/Werkstatt** von April bis Juni (ca. 570 bzw. 710), auch ohne Neustart – unklar, ob echt.
- **Betriebszeit-Zähler** springt gelegentlich um genau 31 min zurück.
- **Schlafzimmer** ist ein anderer Sensortyp („RQ“ laut Jonas; Nachkommastellen, keine Betriebszeit) – nicht 1:1 mit den anderen Radonsensoren vergleichbar.
- **Lücke** Technikraum/Werkstatt 11.–13.06. (38,7 h); Wetterdaten mit Lücken bis 14 h.
- **Winter-Werte** (1 060 / 54 / 94 Bq/m³) sind Extrapolation aus Sommerdaten und Temperatur-Regression, keine Messung.
- **Luftwechsel konstant** angenommen; im Winter (stärkeres Lüften, Temperaturunterschied) dürfte er höher sein, daher sind die Winter-Werte eine Obergrenze.
- **Hausvolumen** 675 m³ ist eine Angabe des Hausbesitzers, nicht vermessen.
- **Quellen 400/200 Bq/m³ und Frist 2018** (österreichische Grenzwerte) stammen nur aus Sekundärquellen, nicht aus dem Originaltext.
- **Länderklassen der Weltkugel** sind aus Karten abgelesen (Zielinski & Chambers 2008, Daten bis 2007), nicht exakt und nicht aktuell. Sie zeigen Größenordnungen, keine Messwerte.
- **Ländergrenzen** (Natural Earth 1:110m) sind grob und nur für die Übersicht gedacht; Grenzen und Namen entsprechen nicht jeder politischen Sicht.
- **UNSCEAR-Tabelle** selbst nicht lesbar; das Weltmittel 39 Bq/m³ stammt aus dem Zitat in Zielinski & Chambers (UNSCEAR 2000).
