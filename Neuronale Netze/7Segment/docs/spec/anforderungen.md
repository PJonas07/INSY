# Anforderungen – 7Segment

Stand: 2026-09-29 (von Claude aus dem Auftrag abgeleitet, keine Lehrkraft-Vorgaben)

## §1 Aufgabe
Ein neuronales Netz erhält die 7 Segmente (a–g, jeweils 0/1) und gibt aus, welche Ziffer 0–9 angezeigt wird.

## §2 Netz
- Aufbau 7 → 8 → 10, vollständig verbunden, Sigmoid in beiden Schichten.
- Selbst implementiert mit NumPy (kein ML-Framework).
- Training: Backpropagation, Batch-Gradientenabstieg, Fehler E = ½·Σ(y − t)², gemittelt über die Beispiele.
- Seed fest (reproduzierbar); nach dem Training werden alle 10 Ziffern richtig erkannt.

## §3 Anzeige / Hintergrundsimulation (Python)
- Klickbare 7-Segment-Anzeige.
- Netzgraph: Knoten nach Aktivierung, Kanten nach Gewicht (Vorzeichen + Betrag).
- Schrittweise Berechnung jedes Knotens mit angezeigter Formel.
- Live-Training mit Fehlerkurve.

## §4 HTML-Visualisierung
- Eigenständige Datei ohne Internet, nutzt die trainierten Gewichte.
- Gleiche Funktionen wie §3 außer Live-Training; zusätzlich Trainings-Fehlerkurve.
- Hell/Dunkel, Tastaturbedienung, responsiv.
