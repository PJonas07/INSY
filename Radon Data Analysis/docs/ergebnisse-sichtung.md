# Ergebnisse der Datensichtung – Radon-Messdaten

Stand: 2026-10-13 · Datei: `Dataset/radon_sample_data.csv`

Dieses Dokument fasst zusammen, was beim Durchsehen der Messdaten aufgefallen ist (Abschnitte 1–8), und erklärt den Hintergrund zu Radon (Abschnitt 9). Die Kennzahlen der Website rechnet `scripts/build_site_data.py`; die übrigen Zahlen stammen aus einmaligen Auswertungen.

**So wurde gerechnet:** Alle Radonwerte sind in Bq/m³. Verglichen werden Stundenmittel. Entfernt wurden nur die 0-Werte, die ein Gerät direkt nach einem Neustart meldet. Was nur eine Vermutung ist, steht ausdrücklich als Vermutung da.

## 1. Kurzfassung

1. **Das Haus ist im Alltag wenig belastet.** Die Wohnräume liegen im Mittel bei 28–43 Bq/m³. Der österreichische Referenzwert liegt bei 300 Bq/m³ im Jahresmittel.
2. **Im Urlaub (31.07.–06.08.) steigt Radon auf gut das Achtfache** (Wohnräume im Mittel 310 statt 37 Bq/m³). Alle Räume liegen dann im Mittel bei 260–360 Bq/m³. Nach der Rückkehr fällt der Wert binnen etwa 1,5 Stunden auf unter 25.
3. **Am stärksten betroffen** sind im Alltag Werkstatt und Technikraum, im Urlaub der Küchensockel und das Schlafzimmer.
4. **Die Wohnraumlüftung wurde vermutlich am 30./31.03. in Betrieb genommen.** Die Küche fällt von 194 auf 42 Bq/m³ im Mittel.
5. **Vermutung:** Im Urlaub und am 20.07. war die Lüftung aus oder gedrosselt. Das muss der Hausbesitzer bestätigen.

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

## 5. Die Wohnraumlüftung

### Vermuteter Einbau: 30./31.03.2026

| Zeitraum | Büro | Küche | Wohnzimmer |
|---|---:|---:|---:|
| 24.–30.03. | 62 | 194 | 136 |
| 31.03.–30.04. | 39 | 42 | 47 |
| 07.08.–13.10. | 26 | 27 | 30 |

Tagesmittel der Küche rund um den Sprung: 24.03. 568, 25.03. 269, 28.03. 224, 30.03. 144, 31.03. 56, 06.04. 19. Die ersten Messwerte überhaupt liegen bei 540–560, der höchste Einzelwert bei 707.

Einschränkung: Vor dem Sprung gibt es nur sechs Tage Daten, und das von einem bis drei Sensoren. Der Sprung ist deutlich, das Datum aber eine Vermutung.

### Die Lüftung wirkt, solange sie läuft

Nächte, in denen sich Radon in den Wohnräumen staut (Mittel von 3 bis 6 Uhr über 90):

| Monat | März | April | Mai | Juni | Juli | August | September | Oktober |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Nächte über 90 | 3 von 4 | 6 von 30 | 2 von 31 | 5 von 30 | 0 von 31 | 7 von 31 | 0 von 30 | 0 von 13 |

Sechs der sieben August-Nächte gehören zum Urlaub. Seit dem 07.08. gab es nur noch eine solche Nacht (23.08.).

### Vermutung: Lüftung im Urlaub und am 20.07. aus

Bei laufender Überdrucklüftung dürfte Radon in einem leeren Haus nicht steigen. Genau das passiert aber zweimal:

- **Urlaub 31.07.–06.08.:** Anstieg auf 260–360 im Mittel, Abfall binnen 1,5 Stunden nach der Rückkehr.
- **Mo 20.07.:** Ab 8 Uhr steigt Radon gleichmäßig, bis 23 Uhr auf 253 (Küche), 274 (Wohnzimmer) und 502 (Küche-Sockel). Um Mitternacht fällt es wieder, um 2 Uhr liegt die Küche bei 42.

Beide Male passt das Muster zu einer ausgeschalteten oder gedrosselten Lüftung. Belegen lässt sich das aus den Daten nicht.

### Der Überdruck ist nicht messbar

Die Differenz zwischen Innendruck und Wetterdruck schwankt um etwa ±0,5 hPa, also ±50 Pa. Der Überdruck einer Lüftung liegt bei wenigen Pa. Auch im Moment der Rückkehr am 06.08. ist kein Drucksprung zu sehen. Die Wetterdaten sind dafür zu grob (stündlich, anderer Standort).

## 6. Weitere Auffälligkeiten

- **Zwei Raumgruppen.** Büro, Küche, Wohnzimmer und Schlafzimmer verlaufen fast gleich (Korrelation 0,90–0,97). Technikraum und Werkstatt sind untereinander praktisch identisch (0,98), hängen mit den Wohnräumen aber nur lose zusammen (etwa 0,55).
- **Technikraum und Werkstatt gehen eigene Wege.** Bis Mitte Mai liegen sie bei etwa 10. Später gibt es mehrtägige Phasen mit 150–250, während die Wohnräume bei etwa 30 bleiben: 25.–27.05., 09.–14.08. und 16.–21.08. Vermutung: Diese Räume liegen außerhalb des Überdruckbereichs.
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

1. Wann wurde die Wohnraumlüftung eingebaut oder eingeschaltet? Passt der 30./31.03.?
2. War die Lüftung im Urlaub (31.07.–06.08.) und am 20.07. aus oder gedrosselt?
3. Wo liegen Technikraum und Werkstatt, und sind sie an die Lüftung angeschlossen?
4. Was ist am 16.04., 06.07., 30.08., 10.09. und 16.09. passiert (Stromausfall, Update)?
5. Sind die vielen 0-Werte in Technikraum und Werkstatt von April bis Juni plausibel?

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

- [WHO: Radon and health](https://www.who.int/news-room/fact-sheets/detail/radon-and-health) – Empfehlung 100/300, Risiko, Eintrittswege
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

Nicht einzeln nachgeprüft sind die Halbwertszeiten der Folgeprodukte (Lehrbuchwerte) und der US-Wert im Originaltext der EPA.
