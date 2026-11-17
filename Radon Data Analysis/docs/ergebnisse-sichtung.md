# Ergebnisse der Datensichtung – Radon-Messdaten

Stand: 2026-11-17 · Datei: `Dataset/radon_sample_data.csv`

Dieses Dokument fasst zusammen, was beim Durchsehen der Messdaten aufgefallen ist (Abschnitte 1–8), und erklärt den Hintergrund zu Radon (Abschnitt 9). Die Kennzahlen der Website rechnet `scripts/build_site_data.py`; die übrigen Zahlen stammen aus einmaligen Auswertungen.

**So wurde gerechnet:** Alle Radonwerte sind in Bq/m³. Verglichen werden Stundenmittel. Entfernt wurden nur die 0-Werte, die ein Gerät direkt nach einem Neustart meldet. Was nur eine Vermutung ist, steht ausdrücklich als Vermutung da.

## 1. Kurzfassung

1. **Das Haus ist im Alltag wenig belastet.** Die Wohnräume liegen im Mittel bei 28–43 Bq/m³. Der österreichische Referenzwert liegt bei 300 Bq/m³ im Jahresmittel.
2. **Im Urlaub (31.07.–06.08.) steigt Radon auf gut das Achtfache** (Wohnräume im Mittel 310 statt 37 Bq/m³). Alle Räume liegen dann im Mittel bei 260–360 Bq/m³. Nach der Rückkehr fällt der Wert binnen etwa 1,5 Stunden auf unter 25.
3. **Am stärksten betroffen** sind im Alltag Werkstatt und Technikraum, im Urlaub der Küchensockel und das Schlafzimmer.
4. **Ab 31.03. waren die Fenster gekippt** (laut Hausbesitzer). Die Küche fällt von 194 auf 42 Bq/m³ im Mittel.
5. **Am 24.08. wurde die Wohnraumlüftung eingebaut** (laut Hausbesitzer). Technikraum und Werkstatt fallen von 162 auf 18 Bq/m³ (−89 %), die Wohnräume von 32 auf 24 (je 14 Tage davor und danach).
6. **Im Urlaub und am 20.07.** gab es noch keine Lüftung, und die Fenster waren zu. Deshalb steigt Radon im leeren Haus.
7. **Das Haus ist sehr dicht.** Im Urlaub lädt sich Radon wie ein Kondensator auf (τ = 40 h, Endwert 377 Bq/m³). Bei geschlossenem Haus wird die Luft nur 1,8 % pro Stunde getauscht; es kommen rund 6 400 Bq pro Stunde herein. Im Winter bei 0 °C wäre ein geschlossenes Haus ohne Lüftung nach etwa 12 h über 300 und käme auf rund 1 060 Bq/m³ (Schätzung). Mit Lüftung bleiben die Wohnräume bei etwa 54 Bq/m³.

## 2. Der Datensatz

| Merkmal | Wert |
|---|---|
| Zeilen / Spalten | 229 403 / 29 |
| Zeitraum | 24.03.2026 bis 13.10.2026 |
| Radonsensoren | Büro, Küche, Küche-Sockel, Schlafzimmer, Technikraum, Werkstatt, Wohnzimmer |
| Raumluft (Druck, Temperatur, CO₂, Feuchte) | Küche und Schlafzimmer |
| Wetter | Temperatur, Luftdruck, Wind, Bodentemperatur in 0, 6 und 54 cm Tiefe |
| Messintervall | Radon und Raumluft etwa 10 Minuten, Wetter 60 Minuten |

Jede Zeile ist die Meldung eines einzelnen Geräts. Fast alle anderen Spalten der Zeile sind leer. Vor jeder Auswertung müssen die Daten deshalb auf ein gemeinsames Zeitraster gebracht werden, zum Beispiel Stundenmittel.

Die Geräte starten zu unterschiedlichen Zeiten:

| Gerät | Erste Messung |
|---|---|
| Küche (Radon) | 24.03. |
| Büro, Wohnzimmer | 27.03. |
| Küche-Sockel | 30.03. |
| Technikraum, Werkstatt | 01.04. |
| Küche (Raumluft) | 08.05. |
| Schlafzimmer (Radon und Raumluft) | 13.05. |
| Luftfeuchte in beiden Räumen | 10.07. |

## 3. Wann war niemand zuhause?

Abwesenheit lässt sich über CO₂ erkennen: Menschen atmen CO₂ aus. Steigt CO₂ in Küche und Schlafzimmer über Stunden nicht an und fällt auf etwa 410 ppm (Außenluft), ist niemand da. CO₂ gibt es erst ab 08.05., davor sind Abwesenheiten nicht erkennbar.

| Zeitraum | Dauer | Woran erkennbar |
|---|---|---|
| Fr 31.07. ca. 05–07 Uhr bis Do 06.08. 20:03 Uhr | etwa 6,5 Tage | Letzter CO₂-Anstieg in der Küche um 05:11 Uhr, danach nur noch gleichmäßiger Abfall bis 410 ppm. Am 06.08. um 20:03 Uhr steigt CO₂ in beiden Räumen sprunghaft. |
| Mo 20.07. ca. 07 bis 24 Uhr | etwa 17 Stunden | Kein CO₂-Anstieg, Küche fällt von 611 auf 497 ppm. |
| So 10.05. abends bis Mo 11.05. ca. 14:40 Uhr | etwa 16 Stunden | Kein CO₂-Anstieg. Radon bleibt unauffällig. |

Zwei Nächte fallen zusätzlich auf, weil das Schlafzimmer nachts kaum CO₂ zeigt: 08.07. (431 ppm) und 28.08. (468 ppm), üblich sind etwa 740 ppm. Das kann eine Nacht außer Haus sein, aber auch ein offenes Fenster.

### Der Urlaub im Detail

| Zeitpunkt | Wohnräume (Mittel aus 5 Sensoren) | Technikraum und Werkstatt |
|---|---:|---:|
| Fr 31.07. 12 Uhr | 74 | 175 |
| Sa 01.08. 00 Uhr | 140 | 176 |
| Sa 01.08. 12 Uhr | 231 | 229 |
| So 02.08. 12 Uhr | 307 | 244 |
| Mo 03.08. 12 Uhr | 366 | 291 |
| Do 06.08. 08 Uhr (Höchstwert) | 395 | – |

Der Anstieg dauert etwa drei Tage, danach bleibt der Wert auf einem Plateau. Die Rückkehr ist sehr deutlich: Das Wohnzimmer fällt von 358 (20:10 Uhr) auf 40 (21:53 Uhr). Gleichzeitig sinkt die Küchentemperatur von 26 auf 24 °C. Die Werkstatt reagiert langsamer und ist erst nach etwa sechs Stunden unter 100.

## 4. Welcher Raum ist am stärksten betroffen?

Verglichen wird nur der Zeitraum, in dem alle sieben Sensoren gleichzeitig messen (ab 13.05., 3 555 Stunden).

### Im Alltag (ohne Urlaub, 3 411 Stunden)

| Rang | Raum | Mittel | Median | Höchstes Stundenmittel | Anteil der Stunden über 100 | Stunden über 300 |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Werkstatt | 60 | 41 | 270 | 18,7 % | 0 |
| 2 | Technikraum | 56 | 38 | 246 | 17,4 % | 0 |
| 3 | Küche-Sockel | 53 | 43 | 502 | 11,0 % | 16 |
| 4 | Schlafzimmer | 43 | 38 | 210 | 2,5 % | 0 |
| 5 | Wohnzimmer | 32 | 27 | 274 | 1,9 % | 0 |
| 6 | Küche | 29 | 24 | 253 | 1,4 % | 0 |
| 7 | Büro | 28 | 23 | 210 | 1,2 % | 0 |

### Im Urlaub (01.–06.08., 144 Stunden)

| Rang | Raum | Mittel | Höchstes Stundenmittel | Stunden über 300 |
|---:|---|---:|---:|---:|
| 1 | Küche-Sockel | 355 | 584 | 115 |
| 2 | Schlafzimmer | 347 | 471 | 115 |
| 3 | Küche | 296 | 387 | 91 |
| 4 | Wohnzimmer | 296 | 394 | 89 |
| 5 | Werkstatt | 284 | 364 | 68 |
| 6 | Technikraum | 267 | 358 | 43 |
| 7 | Büro | 256 | 351 | 59 |

### Was daraus folgt

- **Küche-Sockel ist der einzige Sensor, der auch im Alltag über 300 kommt.** Er misst im selben Raum wie der Küchensensor, liegt aber in 77 % der Stunden höher, im Mittel um 21 Bq/m³. Im Juli ist der Abstand am größten (86 gegen 31). Das passt dazu, dass Radon aus dem Boden kommt und in Bodennähe zuerst ankommt.
- **Das Schlafzimmer** ist unter den Wohnräumen am höchsten. Dort misst allerdings ein anderer Sensortyp („RQ“, Angabe des Projektinhabers), der Vergleich ist deshalb nicht ganz sauber.
- **Das Büro** ist in jeder Lage der am wenigsten belastete Raum.
- **Werkstatt und Technikraum** haben den höchsten Mittelwert, aber keine extremen Spitzen.

## 5. Fenster und Wohnraumlüftung

### Fenster gekippt ab 31.03.2026

| Zeitraum | Büro | Küche | Wohnzimmer |
|---|---:|---:|---:|
| 24.–30.03. | 62 | 194 | 136 |
| 31.03.–30.04. | 39 | 42 | 47 |
| 07.08.–13.10. | 26 | 27 | 30 |

Tagesmittel der Küche rund um den Sprung: 24.03. 568, 25.03. 269, 28.03. 224, 30.03. 144, 31.03. 56, 06.04. 19. Die ersten Messwerte überhaupt liegen bei 540–560, der höchste Einzelwert bei 707.

Ursache laut Hausbesitzer: Bis 30.03. waren die Fenster geschlossen, ab 31.03. gekippt. Die Lüftung gab es zu diesem Zeitpunkt noch nicht. Einschränkung: Vor dem Sprung gibt es nur sechs Tage Daten von einem bis drei Sensoren.

### Lüftung eingebaut am 24.08.2026

Die Lüftung hält im ganzen Haus einen leichten Überdruck. Dadurch strömt keine Bodenluft und damit kein Radon nach. Vergleich der Tagesmittel, je 14 Tage vor und nach dem Einbau (berechnet in `scripts/build_site_data.py`):

| Zeitraum | Wohnräume | Technikraum und Werkstatt |
|---|---:|---:|
| 10.–23.08. | 32 | 162 |
| 24.08.–06.09. | 24 | 18 |

Technikraum und Werkstatt fallen innerhalb eines Tages von über 100 auf etwa 20 und bleiben dort. In den Wohnräumen ändert sich wenig, weil die gekippten Fenster dort schon vorher für niedrige Werte gesorgt haben. Vermutung: Technikraum und Werkstatt werden kaum über Fenster gelüftet, deshalb wirkt dort erst der Überdruck.

### Nächte mit Radonstau

Nächte, in denen sich Radon in den Wohnräumen staut (Mittel von 3 bis 6 Uhr über 90):

| Monat | März | April | Mai | Juni | Juli | August | September | Oktober |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Nächte über 90 | 3 von 4 | 6 von 30 | 2 von 31 | 5 von 30 | 0 von 31 | 7 von 31 | 0 von 30 | 0 von 13 |

Sechs der sieben August-Nächte gehören zum Urlaub. Seit dem 07.08. gab es nur noch eine solche Nacht (23.08., am Tag vor dem Einbau der Lüftung).

### Abwesenheiten: Fenster zu, noch keine Lüftung

Wenn niemand zuhause ist, steigt Radon deutlich. Das passiert zweimal:

- **Urlaub 31.07.–06.08.:** Anstieg auf 260–360 im Mittel, Abfall binnen 1,5 Stunden nach der Rückkehr.
- **Mo 20.07.:** Ab 8 Uhr steigt Radon gleichmäßig, bis 23 Uhr auf 253 (Küche), 274 (Wohnzimmer) und 502 (Küche-Sockel). Um Mitternacht fällt es wieder, um 2 Uhr liegt die Küche bei 42.

Beide Abwesenheiten liegen vor dem 24.08. Es gab also noch keine Lüftung, und die Fenster waren vermutlich geschlossen. Nach der Rückkehr wird wieder gelüftet, und der Wert fällt.

### Der Überdruck ist nicht messbar

Die Differenz zwischen Innendruck und Wetterdruck schwankt um etwa ±0,5 hPa, also ±50 Pa. Der Überdruck einer Lüftung liegt bei wenigen Pa. Auch im Moment der Rückkehr am 06.08. ist kein Drucksprung zu sehen. Die Wetterdaten sind dafür zu grob (stündlich, anderer Standort).

### Wie dicht ist das Haus? Das Kondensator-Modell

Während des Urlaubs (31.07. 06:00 bis 06.08. 20:00) war das Haus leer, die Fenster zu und die Lüftung noch nicht eingebaut. Für Radon gilt dann eine Bilanz:

Änderung pro Stunde = Zustrom − (Luftwechsel + Zerfall) · Konzentration

Die Lösung ist dieselbe Kurve wie beim Laden eines Kondensators über einen Widerstand:

C(t) = C_Ende − (C_Ende − C_Start) · e^(−t/τ), mit τ = 1 / (Luftwechsel + Zerfall)

| Kondensator | Haus |
|---|---|
| Ladespannung U₀ | Endwert C_Ende = Zustrom / (Luftwechsel + Zerfall) |
| Zeitkonstante τ = R · C | τ = 1 / (Luftwechsel + Zerfall) |
| großer Widerstand | dichtes Haus |
| Laden | Haus zu |
| Entladen | Fenster auf |

**Kurvenanpassung** (`fit_exponential` in `scripts/build_site_data.py`): Für jede Rate k auf einem logarithmischen Raster von 0,001 bis 10 pro Stunde ist die Kurve eine Gerade in x = 1 − e^(−k·t). Start und Ende folgen dann aus einer linearen Regression; gewählt wird die Rate mit dem kleinsten Fehler. Radonzerfall: ln 2 / 3,82 Tage = 0,0076 pro Stunde. Hausvolumen laut Hausbesitzer: 3 × 90 m² × 2,5 m = 675 m³.

| Größe | Wohnräume | Technikraum und Werkstatt |
|---|---:|---:|
| Zeitkonstante τ | 40 h | 109 h |
| Startwert / Endwert | 27 / 377 Bq/m³ | 161 / 385 Bq/m³ |
| mittlere Abweichung Modell–Messung | 16,4 Bq/m³ | 12,4 Bq/m³ |
| Luftwechsel (1/τ − Zerfall) | 0,018 pro Stunde | 0,002 pro Stunde |
| Zustrom (Endwert / τ) | 9,5 Bq/(m³·h) | 3,5 Bq/(m³·h) |

Für das ganze Haus (Wohnräume-Werte × 675 m³) sind das rund **6 400 Bq pro Stunde**. Ein Luftwechsel von 0,018 pro Stunde heißt: Die Luft ist erst nach etwa 56 Stunden einmal getauscht. Zum Vergleich gelten für Wohnhäuser meist 0,3 bis 0,5 pro Stunde als ausreichend (Lehrbuchwert, nicht einzeln nachgeprüft). Das Haus ist bei geschlossenen Fenstern also sehr dicht.

**Entladen nach der Rückkehr** (10-Minuten-Werte, 4 Stunden ab 06.08. 20:00): τ = 72 min, Luftwechsel 0,8 pro Stunde, also rund 45-mal so viel wie bei geschlossenem Haus.

### Sommer und Winter

Im Urlaub war es innen 25,0 °C und außen 25,6 °C, es gab also keinen Kamineffekt. Im Winter ist es innen wärmer als außen; die warme Luft steigt auf und zieht unten Bodenluft nach. Das zeigen die Daten seit dem 24.08. (Lüftung an): Pro Grad weniger Außentemperatur steigen die Tagesmittel in den Wohnräumen um 1,5 Bq/m³ und in Technikraum und Werkstatt um 3,5 Bq/m³ (lineare Regression, 51 Tage, außen 3,5 bis 23 °C).

**Schätzung für 0 °C:**

1. *Mit Lüftung:* Gerade bis 0 °C verlängert: Wohnräume etwa 54, Technikraum und Werkstatt etwa 94 Bq/m³.
2. *Ohne Lüftung, Haus zu:* Der Zustrom wächst laut derselben Gerade um rund 8 % pro Kelvin Temperaturunterschied, bei 23 K also auf das 2,8-Fache (`winter_factor`). Mit gleichem τ ergibt das einen Endwert von rund 1 060 Bq/m³; 300 wären nach 12 statt 60 Stunden erreicht.

| Lage | Sommer (gemessen) | Winter bei 0 °C (Schätzung) |
|---|---:|---:|
| Haus zu, ohne Lüftung: Endwert | 377 | ≈ 1 060 |
| Haus zu: 300 erreicht nach | 60 h | 12 h |
| Mit Lüftung: Wohnräume | 24 | ≈ 54 |
| Mit Lüftung: Technikraum und Werkstatt | 18 | ≈ 94 |

Einschränkungen: Die Gerade ist über den gemessenen Bereich hinaus verlängert. Im Winter wird der Luftwechsel durch den Kamineffekt eher größer, der Endwert ohne Lüftung ist deshalb eine Obergrenze. Als Anhaltspunkt aus den Messdaten: Ende März (außen rund 4 °C, Fenster zu, Bewohner da) lagen die Wohnräume bei 100 bis 450 Bq/m³ im Tagesmittel.

## 6. Weitere Auffälligkeiten

- **Zwei Raumgruppen.** Büro, Küche, Wohnzimmer und Schlafzimmer verlaufen fast gleich (Korrelation 0,90–0,97). Technikraum und Werkstatt sind untereinander praktisch identisch (0,98), hängen mit den Wohnräumen aber nur lose zusammen (etwa 0,55).
- **Technikraum und Werkstatt gehen eigene Wege.** Bis Mitte Mai liegen sie bei etwa 10. Später gibt es mehrtägige Phasen mit 150–250, während die Wohnräume bei etwa 30 bleiben: 25.–27.05., 09.–14.08. und 16.–21.08. Ab dem Einbau der Lüftung am 24.08. verschwinden diese Phasen.
- **Tagesgang in den Wohnräumen.** Höchstwerte gegen 6 Uhr früh, Tiefstwerte gegen 18 Uhr (Küche 70 gegen 31). Technikraum und Werkstatt haben fast keinen Tagesgang.
- **Wetter erklärt wenig.** Luftdruck, Wind und Außentemperatur korrelieren mit Radon in den Wohnräumen unter 0,2. Nur Technikraum und Werkstatt hängen mäßig an der Bodentemperatur in 54 cm Tiefe (0,49).
- **Kein Wochentagsmuster.** Die Mittelwerte liegen an allen sieben Tagen zwischen 37 und 43.

## 7. Datenqualität

- **0-Werte nach Neustart.** Fällt der Betriebszeit-Zähler auf 0, meldet das Gerät zunächst 0 Bq/m³. Das sind Artefakte und müssen vor jeder Auswertung entfernt werden.
- **Gemeinsame Neustarts.** Am 16.04., 06.07., 30.08., 10.09. und 16.09. starten fast alle Geräte gleichzeitig neu.
- **Viele 0-Werte ohne Neustart.** Technikraum 567, Werkstatt 712, fast alle von April bis Juni. Ob das echte Messwerte sind, ist offen.
- **Zähler springt zurück.** Die Betriebszeit fällt mehrmals um genau 31 Minuten, ohne dass ein Neustart folgt.
- **Schlafzimmer ist ein anderer Sensortyp („RQ“).** Er liefert Nachkommastellen und hat keine Betriebszeit. Bestätigt vom Projektinhaber; die genaue Modellbezeichnung ist noch offen.
- **Lücken.** Technikraum und Werkstatt fehlen vom 11. bis 13.06. für 38,7 Stunden. Die Wetterdaten haben Lücken bis 14 Stunden.

## 8. Offene Fragen an den Hausbesitzer

1. ~~Wann wurde die Wohnraumlüftung eingebaut?~~ Geklärt: am 24.08.; der Sprung am 30./31.03. kam von gekippten Fenstern.
2. Wo liegen Technikraum und Werkstatt, und werden sie über Fenster gelüftet?
3. Was ist am 16.04., 06.07., 30.08., 10.09. und 16.09. passiert (Stromausfall, Update)?
4. Sind die vielen 0-Werte in Technikraum und Werkstatt von April bis Juni plausibel?

## 9. Hintergrund: Radon allgemein

Dieser Abschnitt stammt nicht aus den Messdaten, sondern aus den unten genannten Quellen.

### Warum Radon schadet

Radon ist nicht giftig wie ein Gift, es ist radioaktiv. Chemisch reagiert das Edelgas mit nichts, und das meiste eingeatmete Radon atmet man wieder aus.

Gefährlich sind die Zerfallsprodukte:

1. Aus Radon entstehen Polonium, Blei und Bismut. Das sind keine Gase mehr, sondern winzige Metallteilchen.
2. Sie heften sich an Staub, werden eingeatmet und bleiben in den Bronchien hängen.
3. Dort zerfallen sie und senden Alphastrahlung aus. Alphastrahlung kommt im Gewebe nur Bruchteile eines Millimeters weit, gibt ihre ganze Energie aber genau dort ab.
4. Die Strahlung trifft die Zellen der Bronchialschleimhaut und kann deren Erbgut schädigen. Daraus kann nach Jahren Lungenkrebs entstehen.

Zahlen dazu:

- Das Lungenkrebsrisiko steigt um etwa 16 % je 100 Bq/m³ im Langzeitmittel (WHO).
- Je nach Land gehen 3 bis 14 % der Lungenkrebsfälle auf Radon zurück (WHO).
- In Österreich sind es rund 10 % der Lungenkrebstodesfälle. Nach dem Rauchen ist Radon die zweithäufigste Ursache (AGES).
- Im Freien liegt Radon bei 5 bis 15 Bq/m³ (WHO).

### Wie ernst ist das? 100 gegen 1 000 Bq/m³

Die größte europäische Studie (Darby u. a. 2005, 13 Fall-Kontroll-Studien, 7 148 Lungenkrebsfälle, 14 208 Kontrollen) fand:

- 8,4 % mehr Risiko je 100 Bq/m³ gemessenem Radon, 16 % nach Korrektur der Messunsicherheit (Langzeitmittel).
- Der Zusammenhang ist linear, ohne Schwelle; er gilt auch unter 200 Bq/m³.
- Der Anteil ist für Raucher und Nichtraucher gleich. Raucher haben aber ein etwa 25-mal so hohes Grundrisiko.

Risiko, bis 75 an Lungenkrebs zu sterben:

| Radon im Langzeitmittel | Risiko gegenüber 0 | Nichtraucher | Raucher |
|---|---:|---:|---:|
| 0 Bq/m³ | 1,0-fach | 0,4 % | 10 % |
| 100 Bq/m³ | 1,16-fach | 0,5 % | 12 % |
| 400 Bq/m³ | 1,64-fach | 0,7 % | 16 % |
| 1 000 Bq/m³ (eigene Hochrechnung: 1 + 0,16 · 10) | 2,6-fach | ≈ 1,0 % | ≈ 26 % |

Für dieses Haus (Alltag rund 37 Bq/m³) ergibt das etwa das 1,06-Fache. Die Urlaubswoche ändert am Jahresmittel kaum etwas.

### Andere Organe, Kinder und Jugendliche

- **WHO:** Außer Lungenkrebs ist bisher kein Krebsrisiko und keine andere Wirkung belegt. Andere Organe bekommen eine viel kleinere Dosis. Für Magenkrebs durch Radon im Trinkwasser fanden Studien keinen Zusammenhang.
- **Kinder (Kendall & Smith, UKHSA):** Die Dosis pro eingeatmeter Menge ist bei Kindern größer, weil sie aber weniger Luft einatmen, ist die Jahresdosis ähnlich wie bei Erwachsenen.
- **Leukämie bei Kindern:** Die UK Childhood Cancer Study fand keinen Zusammenhang mit Radon.
- **Folgerung:** Es zählt die Summe über das Leben; wer früh in einem belasteten Haus wohnt, sammelt mehr Jahre an.

### Halbwertszeit

Radon-222 hat eine Halbwertszeit von 3,8 Tagen (genauer 3,82). Nach dieser Zeit ist die Hälfte zerfallen. Das ist lang genug, um aus dem Boden ins Haus zu wandern, und kurz genug, dass ständig Strahlung entsteht.

| Stoff | Halbwertszeit | Strahlung | Form |
|---|---|---|---|
| Radon-222 | 3,8 Tage | Alpha | Gas |
| Polonium-218 | 3,1 Minuten | Alpha | Metallteilchen |
| Blei-214 | 27 Minuten | Beta | Metallteilchen |
| Bismut-214 | 20 Minuten | Beta | Metallteilchen |
| Polonium-214 | 0,00016 Sekunden | Alpha | Metallteilchen |
| Blei-210 | 22 Jahre | Beta | Metallteilchen |

Bezug zu den Messdaten: Nach dem Urlaub fiel das Radon im Wohnzimmer in gut anderthalb Stunden von 358 auf 40 Bq/m³. Durch Zerfall allein hätte das etwa zwölf Tage gedauert (gut drei Halbwertszeiten). Das Radon ist also nicht zerfallen, es wurde hinausgelüftet.

### Woher die 300 Bq/m³ kommen

1. **Strahlenschutz:** Die Internationale Strahlenschutzkommission (ICRP, Publikation 126) hält eine Dosis in der Größenordnung von 10 Millisievert pro Jahr für die Obergrenze in Wohnungen. Umgerechnet auf Radon in der Raumluft ergibt das rund 300 Bq/m³.
2. **WHO (2009):** Empfohlen wird ein Referenzwert von 100 Bq/m³ und, wo das nicht erreichbar ist, höchstens 300.
3. **EU:** Die Richtlinie 2013/59/Euratom (Artikel 74) schreibt allen Mitgliedstaaten einen Referenzwert von höchstens 300 Bq/m³ im Jahresmittel vor.
4. **Österreich:** Strahlenschutzgesetz 2020 und Radonschutzverordnung (BGBl. II Nr. 470/2020) übernehmen genau diese Obergrenze: 300 Bq/m³ im Jahresmittel für Aufenthaltsräume und Arbeitsplätze.

**Vorgeschichte in Österreich:** Bis 2020 gab es für Wohnungen keinen gesetzlichen Wert. Man orientierte sich an der EU-Empfehlung 90/143/Euratom (1990): 400 Bq/m³ für bestehende Gebäude, 200 Bq/m³ als Planungswert für Neubauten. Gesetzlich geregelt waren nur bestimmte Arbeitsplätze (Natürliche Strahlenquellen-Verordnung). Auslöser der Änderung waren die großen Sammelstudien um 2005 (Risiko ohne Schwelle, auch unter 200 Bq/m³). Danach senkte die WHO 2009 ihre Empfehlung auf 100 Bq/m³, die EU schrieb 2013 höchstens 300 Bq/m³ vor (Umsetzung bis Februar 2018), und Österreich setzte das 2020 um. Für bestehende Häuser sank der Wert damit von 400 auf 300 Bq/m³.

Ein Referenzwert ist kein Grenzwert. Darunter ist man nicht automatisch sicher, und darüber drohen keine Strafen. Er sagt, ab wann man etwas unternehmen soll. Weil er für das Jahresmittel gilt, überschreitet ihn eine Woche mit 350 Bq/m³ wie im Urlaub nicht.

### Andere Länder

| Land | Wert für Wohnräume in Bq/m³ | Anmerkung |
|---|---:|---|
| WHO-Empfehlung | 100 | falls nicht erreichbar: höchstens 300 |
| USA | 148 | Aktionswert der Umweltbehörde EPA (4 pCi/L) |
| Kanada | 200 | seit 2007, davor 800 |
| Großbritannien | 200 | Zielwert nach einer Sanierung: 100 |
| Schweden | 200 | seit 2004, davor 400 |
| Deutschland | 300 | Strahlenschutzgesetz |
| Schweiz | 300 | seit 2018, davor 1 000 |
| Österreich | 300 | Radonschutzverordnung 2020 |

Kanada: In der landesweiten Messung von 2012 lebten 6,9 % der Bevölkerung in Häusern über 200 Bq/m³. Eine neuere Auswertung von 2024 kommt auf 17,8 % der Häuser. Mit 37 Bq/m³ im Alltag läge das hier gemessene Haus auch nach kanadischem Maßstab weit darunter.

### Hotspots

Entscheidend ist der Untergrund: viel Uran im Gestein, etwa in Granit, und ein Boden, der Gas gut durchlässt.

- **Österreich:** Am stärksten betroffen ist das Granitbergland im Mühlviertel und im Waldviertel, dazu Teile Tirols und der Steiermark. 104 Gemeinden sind Radonschutzgebiet.
- **Umhausen im Ötztal:** In einem Ortsteil lag der Median im Erdgeschoß bei 1 868 Bq/m³, im restlichen Ort bei 182 (Studie von 1994). Der Ortsteil steht auf lockerem Material eines alten Bergsturzes.
- **Kanada:** Bei der Messung von 2012 lagen die meisten Häuser über dem Richtwert in New Brunswick (24,8 %), Manitoba (23,7 %), im Yukon (19,6 %) und in Saskatchewan (16,3 %).

### Bauweise

- **Der Weg ins Haus:** Radon kommt durch Risse im Boden, durch Fugen zwischen Boden und Wand und durch undichte Rohr- und Kabeldurchführungen.
- **Der Kamineffekt:** Warme Luft steigt im Haus nach oben. Unten entsteht ein leichter Unterdruck, der Bodenluft ansaugt, am stärksten im Winter. Räume mit Erdkontakt sind deshalb am meisten belastet. Dazu passt, dass der Sensor am Küchensockel die höchsten Werte zeigt.
- **Dichtheit wirkt in beide Richtungen:** Eine dichte Bodenplatte hält Radon draußen. Dichte Fenster und Wände halten es drinnen; nach einer thermischen Sanierung können die Werte steigen.
- **Neubau:** durchgehende Fundamentplatte von mindestens 20 cm, dichte Durchführungen, bei Bedarf eine Radondrainage, die Bodenluft über das Dach abführt.
- **Bestand:** Bodenplatte abdichten oder die Bodenluft darunter absaugen. Einfache Maßnahmen kosten wenige hundert Euro, aufwendige bis etwa 15 000 Euro (AGES).
- **Überdrucklüftung wie in diesem Haus:** Sie dreht den Kamineffekt um. Die Luft drückt nach außen, statt Bodenluft anzusaugen.

### Quellen

- [WHO: Radon and health](https://www.who.int/news-room/fact-sheets/detail/radon-and-health) – Empfehlung 100/300, Risiko, Eintrittswege, keine anderen gesicherten Wirkungen
- [Darby u. a. 2005, BMJ (PubMed)](https://pubmed.ncbi.nlm.nih.gov/15613366/) – 8,4 % bzw. 16 % je 100 Bq/m³, Risiko bis 75 Jahre
- [Kendall & Smith: Doses from radon to children](https://researchportal.ukhsa.gov.uk/en/publications/doses-from-radon-and-its-decay-products-to-children/) – Dosis bei Kindern
- [UK Childhood Cancer Study: radon gas](https://eprints.whiterose.ac.uk/85715/1/The%20United%20Kingdom%20Childhood%20Cancer%20Study%20of%20exposure%20to%20domestic%20sources%20of%20ionising%20radiation%3A%201%3A%20radon%20gas..pdf) – kein Zusammenhang mit Kinderkrebs
- [Radonschutzverordnung, BGBl. II Nr. 470/2020](https://ris.bka.gv.at/Dokumente/BgblAuth/BGBLA_2020_II_470/BGBLA_2020_II_470.rtf) – 300 Bq/m³
- [Land Oberösterreich: Radonvorsorge](https://www.land-oberoesterreich.gv.at/files/publikationen/us_radon_vorsorge_neubauten_sanierung.pdf) – frühere Richtwerte 400/200 Bq/m³
- [AWMF-Leitlinie „Radon in Innenräumen“, 2022](https://register.awmf.org/assets/guideline_bkp/002-035l_S1_Radon-in-Innenraeumen_2022-02.pdf) – Halbwertszeit, Zerfallsprodukte, Wirkung in der Lunge
- [ICRPaedia: Radon progeny](https://icrpaedia.org/Radon_progeny) – Zerfallsreihe
- [ICRP Publication 126](https://icrpaedia.org/ICRP_Publication_126) – 300 Bq/m³ und 10 mSv pro Jahr
- [Richtlinie 2013/59/Euratom, Artikel 74](https://www.legislation.gov.uk/eudr/2013/59/article/74) – EU-Obergrenze
- [AGES: Radon](https://www.ages.at/umwelt/radioaktivitaet/radon) – Österreich, Bauweise, Maßnahmen
- [AGES: Europäischer Radontag](https://www.ages.at/ages/presse/news/detail/7-november-ist-europaeischer-radontag) – Lungenkrebs, 104 Gemeinden
- [Erläuterungen zur Radonschutzverordnung (WKO)](https://news.wko.at/oe/news/radonschutzv--erlaeuterungen.pdf) – Referenzwert in Österreich
- [Health Canada: Cross-Canada Survey 2012](https://www.canada.ca/en/health-canada/services/environmental-workplace-health/reports-publications/radiation/cross-canada-survey-radon-concentrations-homes-final-report-health-canada-2012.html) – Richtwert und Provinzen
- [Health Canada: Radon action guide](https://www.canada.ca/en/health-canada/services/health-risks-safety/radiation/radon/action-guides/provinces-territories.html) – Auswertung 2024
- [Studie zu Umhausen, 1994](https://pubmed.ncbi.nlm.nih.gov/8026968/) – Messwerte im Ötztal
- [UKHSA: Radon levels](https://www.ukradon.org/information/level), [BAG Schweiz](https://www.bag.admin.ch/de/gesetzliche-bestimmungen-bezueglich-radon), [LfU Bayern](https://www.lfu.bayern.de/strahlung/radon_in_gebaeuden/faq_radon/index.htm), [Strålsäkerhetsmyndigheten](https://aarst.org/wp-content/uploads/2026/01/AARST_2025_Panel_Discussion_Sweden_Ronnqvist.pdf) – Werte anderer Länder
- [Zielinski & Chambers 2008: Mapping of Residential Radon in the World](https://www.osti.gov/etdeweb/servlets/purl/21510212) – Landesmittel weltweit (Karten, WHO-IRP-Daten bis 2007), Weltmittel 39 Bq/m³ (UNSCEAR 2000, dort zitiert)

Nicht im Originaltext gelesen (nur über Zusammenfassungen und Suchergebnisse): die Werte 400/200 Bq/m³ der EU-Empfehlung 90/143/Euratom, die Umsetzungsfrist Februar 2018 und die Kinderstudien. Nicht einzeln nachgeprüft sind außerdem die Halbwertszeiten der Folgeprodukte (Lehrbuchwerte) und der US-Wert im Originaltext der EPA.
