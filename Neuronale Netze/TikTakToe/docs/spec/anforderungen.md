# Anforderungen – TikTakToe

Stand: 2026-10-13 · von Claude aus dem Auftrag abgeleitet, keine Lehrkraft-Vorgaben bekannt · von Jonas nicht im Einzelnen bestätigt (Antwort auf die Rückfrage: „Mit Git; Führe das Projekt aus“)

## §1 Aufgabe
Ein neuronales Netz erhält ein Tic-Tac-Toe-Spielfeld (9 Felder) und gibt aus, auf welches Feld der Spieler am Zug setzen soll.

## §2 Daten
- Eingabe: 9 Werte aus Sicht des Spielers am Zug: 1 = eigener Stein, −1 = Stein des Gegners, 0 = leer.
- Ziel: 9 Werte, 1 für jedes Feld, das laut Minimax ein bester Zug ist, sonst 0 (mehrere beste Züge möglich).
- Datensatz: alle 4520 nicht beendeten Stellungen, die vom leeren Feld aus erreichbar sind.
- Minimax bevorzugt schnelle Siege und späte Niederlagen.

## §3 Netz
- Aufbau 9 → 36 → 9, vollständig verbunden, Sigmoid in beiden Schichten.
- Selbst implementiert mit NumPy (kein ML-Framework), gleiche Mathematik wie 7Segment.
- Training: Backpropagation, Batch-Gradientenabstieg, Fehler E = ½·Σ(y − t)², gemittelt über die Beispiele. Seed fest.
- Gewählter Zug = leeres Feld mit der höchsten Ausgabe.
- Qualität wird gemessen und ehrlich angezeigt: Anteil bester Züge, verlorene Spielverläufe gegen jeden möglichen Gegner.

## §4 Website (Oberfläche)
- Eigenständige Datei ohne Internet, nutzt die in Python trainierten Gewichte.
- Spielfeld: gegen das Netz spielen; die Ausgabe des Netzes ist pro Feld sichtbar.
- Netzgraph: Knoten nach Aktivierung, Kanten nach Gewicht (Vorzeichen + Betrag); Rechnung eines Knotens als Formel.
- **Training sichtbar:** Die Gewichte werden während des Trainings in Abständen gespeichert. Die Website spielt den Verlauf ab (Regler + Abspielen): Kanten ändern sich, Änderungen seit dem letzten Stand werden hervorgehoben, Fehler- und Trefferkurve laufen mit.
- Hell/Dunkel, Tastaturbedienung, responsiv (nach `DESIGN.md`).

## §5 Python
- Training in der Konsole (`python -m tic_tac_toe.train`), schreibt Modell und Web-Daten.
- Spiel in der Konsole gegen das Netz (`python -m tic_tac_toe.play`).
- Keine tkinter-App (Oberfläche ist die Website).
