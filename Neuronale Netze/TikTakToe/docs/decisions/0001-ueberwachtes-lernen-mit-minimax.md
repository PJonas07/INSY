# ADR-0001: Das Netz lernt überwacht von Minimax

- **Datum:** 2026-10-13
- **Status:** angenommen (Vorschlag von Claude, von Jonas nicht ausdrücklich bestätigt)
- **Beteiligt:** Jonas, Claude

## Kontext

Auftrag: Tic-Tac-Toe „wie 7Segment“ umsetzen. Bei 7Segment gibt es zu jeder Eingabe eine feste richtige Antwort. Bei einem Spiel muss erst festgelegt werden, was „richtig“ ist. Jeder Rechenschritt soll erklärbar bleiben.

## Optionen

1. **Überwachtes Lernen mit Minimax als Lehrer** – Minimax berechnet für jede der 4520 Stellungen die besten Züge, das Netz lernt diese Tabelle. Gleiche Mathematik wie 7Segment (Sigmoid, Fehler ½·Σ(y − t)², Backpropagation). Nachteil: Das Netz findet nichts selbst heraus, es ahmt nach.
2. **Reinforcement Learning (Selbstspiel)** – das Netz lernt nur aus Sieg und Niederlage. Näher an „lernt spielen“, aber neue Konzepte (Belohnung, Exploration), schwankende Ergebnisse, schwerer zu erklären und zu testen.
3. **Stellung bewerten statt Zug wählen** – Netz sagt „X gewinnt / Remis / O gewinnt“. Einfach, aber zum Spielen bräuchte man zusätzlich eine Suche.

## Entscheidung

Option 1. Sie nutzt genau das, was aus 7Segment schon bekannt ist, und das Ergebnis lässt sich exakt messen (Anteil bester Züge, verlorene Spielverläufe).

## Folgen

- Minimax muss selbst programmiert und getestet werden (`minimax.py`).
- Das Netz ist höchstens so gut wie der Lehrer und erreicht ihn nicht ganz (97,1 %).
- Ziel sind mehrere Einsen pro Stellung; deshalb Sigmoid pro Ausgabe statt „genau eine Klasse“.
