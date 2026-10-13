# ADR-0001: Netz selbst mit NumPy programmieren

- **Datum:** 2026-09-29
- **Status:** angenommen
- **Beteiligt:** Jonas, Claude

## Kontext

Schulprojekt: Jeder Rechenschritt muss erklärbar sein. Die Visualisierung soll jeden einzelnen Knoten zeigen.

## Optionen

1. **NumPy, selbst programmiert** – jede Formel im Code sichtbar, eine kleine Dependency. Mehr Code als ein Framework.
2. **PyTorch / scikit-learn** – wenig Code, aber Backpropagation versteckt, große Dependency.
3. **Reines Python** – keine Dependency, aber Matrizenrechnung per Schleifen, mehr und langsamerer Code.

## Entscheidung

Option 1 (von Jonas gewählt). Beste Balance aus Verständlichkeit und Kürze.

## Folgen

- Gradienten müssen selbst hergeleitet werden → durch numerischen Gradienten-Test abgesichert.
- GUI mit tkinter (Standardbibliothek), HTML ohne Frameworks → keine weiteren Dependencies.
