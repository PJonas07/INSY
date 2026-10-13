"""Desktop app: 7-segment display, live network graph and step-by-step calculation.

Run from the project folder:  python -m seven_segment.gui

Layout:
    left    clickable 7-segment display + buttons for the digits 0-9
    middle  network graph (nodes coloured by activation, edges by weight) + calculation text
    right   output neurons as bars, recognised digit, loss curve of the live training
"""

import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk

import numpy as np

from seven_segment import config
from seven_segment.dataset import SEGMENT_NAMES, load_inputs, load_targets, segments_for_digit
from seven_segment.network import NeuralNetwork
from seven_segment.simulation import HIDDEN_LAYER, NodeStep, compute_steps

# ---------------------------------------------------------------------------- design tokens
# Spacing on a 4-pt grid and colours by role (see ~/Programming/Claude/DESIGN.md).
SPACING_S = 8
SPACING_M = 16
SPACING_L = 24

FONT_FAMILY = "Helvetica"
FONT_MONO = "Menlo"
FONT_SMALL = (FONT_FAMILY, 12)
FONT_BODY = (FONT_FAMILY, 14)
FONT_TITLE = (FONT_FAMILY, 20, "bold")
FONT_DIGIT = (FONT_FAMILY, 40, "bold")
FONT_CODE = (FONT_MONO, 12)
FONT_NODE = (FONT_FAMILY, 9)


@dataclass(frozen=True)
class Theme:
    background: str
    surface: str
    text: str
    text_muted: str
    accent: str
    negative: str
    highlight: str
    border: str
    on_accent: str


LIGHT_THEME = Theme(
    background="#FFFFFF",
    surface="#F2F2F7",
    text="#1C1C1E",
    text_muted="#6C6C70",
    accent="#0A64D8",
    negative="#C85A00",
    highlight="#D70015",
    border="#D1D1D6",
    on_accent="#FFFFFF",
)
DARK_THEME = Theme(
    background="#1C1C1E",
    surface="#2C2C2E",
    text="#F2F2F7",
    text_muted="#AEAEB2",
    accent="#409CFF",
    negative="#FF9F0A",
    highlight="#FF6961",
    border="#48484A",
    on_accent="#000000",
)

# ---------------------------------------------------------------------------- behaviour
ANIMATION_DELAY_MS = 350
TRAINING_TICK_MS = 30
EPOCHS_PER_TICK = 10
MAX_EDGE_WIDTH = 4.0
# Weights above this absolute value are all drawn with the maximum line width.
EDGE_WEIGHT_CAP = 6.0


def detect_theme(root: tk.Tk) -> Theme:
    """Use the dark theme when macOS runs in dark mode."""
    try:
        # VERIFY: Tk-internal command, available on macOS with Tk >= 8.6.10 (tested with Tk 9.0).
        is_dark = bool(int(root.tk.call("::tk::unsupported::MacWindowStyle", "isdark", root)))
    except tk.TclError:
        # Not on macOS (or older Tk): no way to ask the system, so fall back to light mode.
        is_dark = False
    return DARK_THEME if is_dark else LIGHT_THEME


def mix_colors(start: str, end: str, amount: float) -> str:
    """Blend two '#RRGGBB' colours; amount 0 -> start, 1 -> end."""
    start_rgb = [int(start[i : i + 2], 16) for i in (1, 3, 5)]
    end_rgb = [int(end[i : i + 2], 16) for i in (1, 3, 5)]
    mixed = [round(s + (e - s) * amount) for s, e in zip(start_rgb, end_rgb, strict=True)]
    return "#" + "".join(f"{value:02X}" for value in mixed)


# ---------------------------------------------------------------------------- 7-segment display


class SegmentDisplay:
    """Canvas with 7 clickable segments."""

    WIDTH = 160
    HEIGHT = 240
    LEFT = 30
    TOP = 20
    LENGTH = 100
    THICKNESS = 16
    GAP = 4

    def __init__(self, parent: tk.Widget, theme: Theme, on_toggle) -> None:
        self.theme = theme
        self.canvas = tk.Canvas(
            parent,
            width=self.WIDTH,
            height=self.HEIGHT,
            background=theme.surface,
            highlightthickness=0,
        )
        self.items: list[int] = []
        for index, points in enumerate(self._segment_polygons()):
            item = self.canvas.create_polygon(points, outline=theme.border, width=1)
            self.canvas.tag_bind(item, "<Button-1>", lambda _event, i=index: on_toggle(i))
            self.items.append(item)

    def _segment_polygons(self) -> list[list[float]]:
        """Polygon points for segments a-g (same order as SEGMENT_NAMES)."""
        x0, x1 = self.LEFT, self.LEFT + self.LENGTH
        y0, y1, y2 = self.TOP, self.TOP + self.LENGTH, self.TOP + 2 * self.LENGTH
        return [
            self._horizontal(x0, x1, y0),  # a
            self._vertical(x1, y0, y1),  # b
            self._vertical(x1, y1, y2),  # c
            self._horizontal(x0, x1, y2),  # d
            self._vertical(x0, y1, y2),  # e
            self._vertical(x0, y0, y1),  # f
            self._horizontal(x0, x1, y1),  # g
        ]

    def _horizontal(self, x_start: float, x_end: float, y: float) -> list[float]:
        half, x_start, x_end = self.THICKNESS / 2, x_start + self.GAP, x_end - self.GAP
        return [
            x_start, y, x_start + half, y - half, x_end - half, y - half,
            x_end, y, x_end - half, y + half, x_start + half, y + half,
        ]  # fmt: skip

    def _vertical(self, x: float, y_start: float, y_end: float) -> list[float]:
        half, y_start, y_end = self.THICKNESS / 2, y_start + self.GAP, y_end - self.GAP
        return [
            x, y_start, x + half, y_start + half, x + half, y_end - half,
            x, y_end, x - half, y_end - half, x - half, y_start + half,
        ]  # fmt: skip

    def show(self, segments: list[int]) -> None:
        for item, is_on in zip(self.items, segments, strict=True):
            self.canvas.itemconfigure(
                item, fill=self.theme.highlight if is_on else self.theme.background
            )


# ---------------------------------------------------------------------------- network graph


class NetworkView:
    """Draws all neurons and connections; shows which neurons are already calculated."""

    WIDTH = 560
    HEIGHT = 440
    NODE_RADIUS = 15
    COLUMN_X = (70, 280, 490)
    MARGIN_Y = 30

    def __init__(self, parent: tk.Widget, theme: Theme) -> None:
        self.theme = theme
        self.canvas = tk.Canvas(
            parent,
            width=self.WIDTH,
            height=self.HEIGHT,
            background=theme.surface,
            highlightthickness=0,
        )
        self.input_positions = self._column(0, config.INPUT_SIZE)
        self.hidden_positions = self._column(1, config.HIDDEN_SIZE)
        self.output_positions = self._column(2, config.OUTPUT_SIZE)

    def _column(self, column: int, count: int) -> list[tuple[float, float]]:
        spacing = (self.HEIGHT - 2 * self.MARGIN_Y) / (count - 1)
        return [(self.COLUMN_X[column], self.MARGIN_Y + i * spacing) for i in range(count)]

    def draw(
        self,
        network: NeuralNetwork,
        segments: list[int],
        steps: list[NodeStep],
        revealed_count: int,
    ) -> None:
        """Redraw everything. Only the first `revealed_count` steps count as calculated."""
        self.canvas.delete("all")
        is_stepping = revealed_count < len(steps)
        current = revealed_count - 1 if is_stepping else None

        hidden_done = min(revealed_count, config.HIDDEN_SIZE)
        output_done = max(0, revealed_count - config.HIDDEN_SIZE)

        self._draw_edges(
            network.weights_hidden,
            self.input_positions,
            self.hidden_positions,
            done_count=hidden_done,
            current=current if current is not None and current < config.HIDDEN_SIZE else None,
            is_stepping=is_stepping,
        )
        output_current = None
        if current is not None and current >= config.HIDDEN_SIZE:
            output_current = current - config.HIDDEN_SIZE
        self._draw_edges(
            network.weights_output,
            self.hidden_positions,
            self.output_positions,
            done_count=output_done,
            current=output_current,
            is_stepping=is_stepping,
        )

        for index, position in enumerate(self.input_positions):
            self._draw_node(position, float(segments[index]), is_current=False)
            self._label(position, SEGMENT_NAMES[index], side=-1)
        for index, position in enumerate(self.hidden_positions):
            value = steps[index].activation if index < hidden_done else None
            self._draw_node(position, value, is_current=index == current)
        for index, position in enumerate(self.output_positions):
            value = steps[config.HIDDEN_SIZE + index].activation if index < output_done else None
            is_current = output_current == index
            self._draw_node(position, value, is_current=is_current)
            self._label(position, str(index), side=1)

        self._draw_column_titles()

    def _draw_edges(
        self,
        weights: np.ndarray,
        sources: list[tuple[float, float]],
        targets: list[tuple[float, float]],
        done_count: int,
        current: int | None,
        is_stepping: bool,
    ) -> None:
        for target_index, (tx, ty) in enumerate(targets):
            # While stepping, only the edges of the neuron being calculated are highlighted.
            if is_stepping:
                is_active = target_index == current
            else:
                is_active = target_index < done_count
            for source_index, (sx, sy) in enumerate(sources):
                weight = weights[source_index, target_index]
                if not is_active:
                    color, width = self.theme.border, 1
                else:
                    color = self.theme.accent if weight >= 0 else self.theme.negative
                    width = 0.5 + min(abs(weight), EDGE_WEIGHT_CAP) / EDGE_WEIGHT_CAP * (
                        MAX_EDGE_WIDTH - 0.5
                    )
                # Negative weights are dashed, so the sign is not shown by colour alone.
                dash = (4, 3) if weight < 0 and is_active else ()
                self.canvas.create_line(sx, sy, tx, ty, fill=color, width=width, dash=dash)

    def _draw_node(self, position: tuple[float, float], value: float | None, is_current: bool):
        x, y = position
        r = self.NODE_RADIUS
        outline = self.theme.highlight if is_current else self.theme.text_muted
        outline_width = 3 if is_current else 1
        if value is None:
            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=self.theme.background, outline=outline, width=outline_width, dash=(2, 2),
            )  # fmt: skip
            self.canvas.create_text(x, y, text="?", fill=self.theme.text_muted, font=FONT_NODE)
            return
        fill = mix_colors(self.theme.background, self.theme.accent, value)
        text_color = self.theme.on_accent if value > 0.5 else self.theme.text
        self.canvas.create_oval(
            x - r, y - r, x + r, y + r, fill=fill, outline=outline, width=outline_width
        )
        self.canvas.create_text(x, y, text=f"{value:.2f}", fill=text_color, font=FONT_NODE)

    def _label(self, position: tuple[float, float], text: str, side: int) -> None:
        x, y = position
        offset = self.NODE_RADIUS + SPACING_S + 4
        anchor = "e" if side < 0 else "w"
        self.canvas.create_text(
            x + side * offset, y, text=text, anchor=anchor, fill=self.theme.text, font=FONT_BODY
        )

    def _draw_column_titles(self) -> None:
        titles = ("Eingabe", "Hidden", "Ausgabe")
        for x, title in zip(self.COLUMN_X, titles, strict=True):
            self.canvas.create_text(
                x, SPACING_S, text=title, anchor="n", fill=self.theme.text_muted, font=FONT_SMALL
            )


# ---------------------------------------------------------------------------- output bars


class OutputView:
    """Horizontal bar per output neuron; the winner is drawn in the accent colour."""

    WIDTH = 260
    HEIGHT = 260
    LABEL_WIDTH = 24
    VALUE_WIDTH = 48

    def __init__(self, parent: tk.Widget, theme: Theme) -> None:
        self.theme = theme
        self.canvas = tk.Canvas(
            parent,
            width=self.WIDTH,
            height=self.HEIGHT,
            background=theme.surface,
            highlightthickness=0,
        )

    def draw(self, outputs: list[float | None]) -> None:
        self.canvas.delete("all")
        known = [value for value in outputs if value is not None]
        winner = int(np.argmax(outputs)) if len(known) == len(outputs) else None
        row_height = self.HEIGHT / len(outputs)
        bar_max = self.WIDTH - self.LABEL_WIDTH - self.VALUE_WIDTH - SPACING_S
        for digit, value in enumerate(outputs):
            top = digit * row_height + 4
            bottom = (digit + 1) * row_height - 4
            middle = (top + bottom) / 2
            self.canvas.create_text(
                SPACING_S, middle, text=str(digit), anchor="w", fill=self.theme.text, font=FONT_BODY
            )
            if value is None:
                self.canvas.create_text(
                    self.LABEL_WIDTH, middle, text="–", anchor="w",
                    fill=self.theme.text_muted, font=FONT_SMALL,
                )  # fmt: skip
                continue
            color = self.theme.accent if digit == winner else self.theme.text_muted
            right = self.LABEL_WIDTH + max(1.0, value * bar_max)
            self.canvas.create_rectangle(
                self.LABEL_WIDTH, top, right, bottom, fill=color, outline=""
            )
            self.canvas.create_text(
                right + 4, middle, text=f"{value:.2f}", anchor="w",
                fill=self.theme.text, font=FONT_SMALL,
            )  # fmt: skip


# ---------------------------------------------------------------------------- loss curve


class LossChart:
    """Line chart of the training error over the epochs."""

    WIDTH = 260
    HEIGHT = 160
    PADDING_LEFT = 44
    PADDING_BOTTOM = 24
    PADDING_TOP = 12
    PADDING_RIGHT = 12

    def __init__(self, parent: tk.Widget, theme: Theme) -> None:
        self.theme = theme
        self.canvas = tk.Canvas(
            parent,
            width=self.WIDTH,
            height=self.HEIGHT,
            background=theme.surface,
            highlightthickness=0,
        )

    def draw(self, losses: list[float], epochs_per_point: int) -> None:
        self.canvas.delete("all")
        left, top = self.PADDING_LEFT, self.PADDING_TOP
        right = self.WIDTH - self.PADDING_RIGHT
        bottom = self.HEIGHT - self.PADDING_BOTTOM
        self.canvas.create_line(left, top, left, bottom, right, bottom, fill=self.theme.border)
        self.canvas.create_text(
            (left + right) / 2, self.HEIGHT - 4, text="Epoche", anchor="s",
            fill=self.theme.text_muted, font=FONT_SMALL,
        )  # fmt: skip
        if len(losses) < 2:
            self.canvas.create_text(
                (left + right) / 2, (top + bottom) / 2, text="Noch kein Training",
                fill=self.theme.text_muted, font=FONT_SMALL,
            )  # fmt: skip
            return

        max_loss = max(losses)
        self.canvas.create_text(
            left - 4, top, text=f"{max_loss:.2f}", anchor="ne",
            fill=self.theme.text_muted, font=FONT_SMALL,
        )  # fmt: skip
        self.canvas.create_text(
            left - 4, bottom, text="0", anchor="e", fill=self.theme.text_muted, font=FONT_SMALL
        )
        self.canvas.create_text(
            right, bottom + 2, text=str(len(losses) * epochs_per_point), anchor="ne",
            fill=self.theme.text_muted, font=FONT_SMALL,
        )  # fmt: skip
        points = []
        for index, loss in enumerate(losses):
            points.append(left + index / (len(losses) - 1) * (right - left))
            points.append(bottom - loss / max_loss * (bottom - top))
        self.canvas.create_line(*points, fill=self.theme.accent, width=2)


# ---------------------------------------------------------------------------- main window


class SevenSegmentApp:
    """Connects the views with the network and handles the buttons."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.theme = detect_theme(root)
        self.inputs = load_inputs()
        self.targets = load_targets()

        self.network, self.loss_history, self.epoch = self._load_network()
        self.segments = segments_for_digit(8)
        self.steps: list[NodeStep] = []
        self.revealed_count = 0
        self.is_training = False
        self.is_animating = False

        self._build_layout()
        self._bind_keys()
        self.recalculate()

    # ------------------------------------------------------------------ setup

    def _load_network(self) -> tuple[NeuralNetwork, list[float], int]:
        """Use the trained model if train.py was run before, otherwise start untrained."""
        if config.MODEL_PATH.exists():
            network, history = NeuralNetwork.load(config.MODEL_PATH)
            return network, history, len(history) * config.LOSS_HISTORY_STEP
        return NeuralNetwork(), [], 0

    def _build_layout(self) -> None:
        theme = self.theme
        self.root.title("7-Segment – Neuronales Netz")
        self.root.configure(background=theme.background)

        style = ttk.Style()
        style.configure("TFrame", background=theme.background)
        style.configure("TLabel", background=theme.background, foreground=theme.text)
        style.configure("Muted.TLabel", foreground=theme.text_muted, font=FONT_SMALL)
        style.configure("Title.TLabel", font=FONT_TITLE)
        style.configure("Digit.TLabel", font=FONT_DIGIT, foreground=theme.accent)

        main = ttk.Frame(self.root, padding=SPACING_L)
        main.grid(sticky="nsew")

        ttk.Label(main, text="7-Segment-Erkennung", style="Title.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, SPACING_M)
        )

        self._build_left_column(main)
        self._build_middle_column(main)
        self._build_right_column(main)
        self._build_controls(main)

    def _build_left_column(self, parent: ttk.Frame) -> None:
        column = ttk.Frame(parent)
        column.grid(row=1, column=0, sticky="n", padx=(0, SPACING_L))
        ttk.Label(column, text="Segmente anklicken (Taste a–g)", style="Muted.TLabel").pack(
            anchor="w"
        )
        self.display = SegmentDisplay(column, self.theme, self.toggle_segment)
        self.display.canvas.pack(pady=SPACING_S)

        ttk.Label(column, text="Ziffer laden (Taste 0–9)", style="Muted.TLabel").pack(
            anchor="w", pady=(SPACING_M, 0)
        )
        digit_grid = ttk.Frame(column)
        digit_grid.pack(pady=SPACING_S)
        for digit in range(10):
            button = ttk.Button(
                digit_grid, text=str(digit), width=2, command=lambda d=digit: self.load_digit(d)
            )
            button.grid(row=digit // 5, column=digit % 5)
        ttk.Button(column, text="Alle aus", command=self.clear_segments).pack(fill="x")

    def _build_middle_column(self, parent: ttk.Frame) -> None:
        column = ttk.Frame(parent)
        column.grid(row=1, column=1, sticky="n")
        ttk.Label(
            column,
            text="Knotenfarbe = Aktivierung · blau = positives Gewicht · "
            "orange gestrichelt = negatives Gewicht",
            style="Muted.TLabel",
        ).pack(anchor="w")
        self.network_view = NetworkView(column, self.theme)
        self.network_view.canvas.pack(pady=SPACING_S)

        self.step_title = ttk.Label(column, text="", font=FONT_BODY)
        self.step_title.pack(anchor="w")
        self.calculation = tk.Text(
            column,
            height=5,
            width=70,
            wrap="word",
            font=FONT_CODE,
            background=self.theme.surface,
            foreground=self.theme.text,
            relief="flat",
            padx=SPACING_S,
            pady=SPACING_S,
        )
        self.calculation.pack(fill="x", pady=(SPACING_S, 0))

    def _build_right_column(self, parent: ttk.Frame) -> None:
        column = ttk.Frame(parent)
        column.grid(row=1, column=2, sticky="n", padx=(SPACING_L, 0))
        ttk.Label(column, text="Ausgabe-Neuronen", style="Muted.TLabel").pack(anchor="w")
        self.output_view = OutputView(column, self.theme)
        self.output_view.canvas.pack(pady=SPACING_S)

        result_row = ttk.Frame(column)
        result_row.pack(fill="x")
        ttk.Label(result_row, text="Erkannt:", font=FONT_BODY).pack(side="left")
        self.result_label = ttk.Label(result_row, text="?", style="Digit.TLabel")
        self.result_label.pack(side="left", padx=SPACING_S)

        ttk.Label(column, text="Fehler (Loss) beim Training", style="Muted.TLabel").pack(
            anchor="w", pady=(SPACING_M, 0)
        )
        self.loss_chart = LossChart(column, self.theme)
        self.loss_chart.canvas.pack(pady=SPACING_S)
        self.training_label = ttk.Label(column, text="", style="Muted.TLabel")
        self.training_label.pack(anchor="w")

    def _build_controls(self, parent: ttk.Frame) -> None:
        controls = ttk.Frame(parent)
        controls.grid(row=2, column=0, columnspan=3, sticky="w", pady=(SPACING_L, 0))
        ttk.Button(controls, text="Nächster Schritt", command=self.next_step).pack(side="left")
        self.animate_button = ttk.Button(
            controls, text="Animation abspielen", command=self.toggle_animation
        )
        self.animate_button.pack(side="left", padx=SPACING_S)
        ttk.Button(controls, text="Sofort berechnen", command=self.reveal_all).pack(side="left")

        self.train_button = ttk.Button(
            controls, text="Training starten", command=self.toggle_training
        )
        self.train_button.pack(side="left", padx=(SPACING_L, SPACING_S))
        ttk.Button(controls, text="Netz zurücksetzen", command=self.reset_network).pack(side="left")

    def _bind_keys(self) -> None:
        for index, name in enumerate(SEGMENT_NAMES):
            self.root.bind(f"<Key-{name}>", lambda _event, i=index: self.toggle_segment(i))
        for digit in range(10):
            self.root.bind(f"<Key-{digit}>", lambda _event, d=digit: self.load_digit(d))
        self.root.bind("<space>", lambda _event: self.next_step())

    # ------------------------------------------------------------------ input actions

    def toggle_segment(self, index: int) -> None:
        self.segments[index] = 1 - self.segments[index]
        self.recalculate()

    def load_digit(self, digit: int) -> None:
        self.segments = segments_for_digit(digit)
        self.recalculate()

    def clear_segments(self) -> None:
        self.segments = [0] * config.INPUT_SIZE
        self.recalculate()

    # ------------------------------------------------------------------ step simulation

    def recalculate(self) -> None:
        """New input or new weights: compute all neuron steps and show the final result."""
        self.is_animating = False
        self.animate_button.configure(text="Animation abspielen")
        self.steps = compute_steps(self.network, np.array(self.segments, dtype=float))
        self.revealed_count = len(self.steps)
        self.refresh()

    def next_step(self) -> None:
        """Reveal one more neuron; after the last one, start again from the beginning."""
        if self.revealed_count >= len(self.steps):
            self.revealed_count = 0
        self.revealed_count += 1
        self.refresh()

    def reveal_all(self) -> None:
        self.is_animating = False
        self.animate_button.configure(text="Animation abspielen")
        self.revealed_count = len(self.steps)
        self.refresh()

    def toggle_animation(self) -> None:
        if self.is_animating:
            self.is_animating = False
            self.animate_button.configure(text="Animation abspielen")
            return
        self.is_animating = True
        self.animate_button.configure(text="Animation stoppen")
        self.revealed_count = 0
        self._animate()

    def _animate(self) -> None:
        if not self.is_animating:
            return
        self.next_step()
        if self.revealed_count >= len(self.steps):
            self.is_animating = False
            self.animate_button.configure(text="Animation abspielen")
            return
        self.root.after(ANIMATION_DELAY_MS, self._animate)

    # ------------------------------------------------------------------ training

    def toggle_training(self) -> None:
        self.is_training = not self.is_training
        self.train_button.configure(
            text="Training stoppen" if self.is_training else "Training starten"
        )
        if self.is_training:
            self._train_tick()

    def _train_tick(self) -> None:
        """Train a few epochs, then redraw; after() keeps the window responsive."""
        if not self.is_training:
            return
        for _ in range(EPOCHS_PER_TICK):
            loss = self.network.train_step(self.inputs, self.targets)
            if self.epoch % config.LOSS_HISTORY_STEP == 0:
                self.loss_history.append(loss)
            self.epoch += 1
        self.recalculate()
        if self.epoch >= config.EPOCHS:
            self.toggle_training()
            return
        self.root.after(TRAINING_TICK_MS, self._train_tick)

    def reset_network(self) -> None:
        """Start again with random (untrained) weights to watch the network learn."""
        if self.is_training:
            self.toggle_training()
        self.network = NeuralNetwork()
        self.loss_history = []
        self.epoch = 0
        self.recalculate()

    # ------------------------------------------------------------------ drawing

    def refresh(self) -> None:
        self.display.show(self.segments)
        self.network_view.draw(self.network, self.segments, self.steps, self.revealed_count)

        outputs: list[float | None] = []
        for index in range(config.OUTPUT_SIZE):
            step_index = config.HIDDEN_SIZE + index
            is_known = step_index < self.revealed_count
            outputs.append(self.steps[step_index].activation if is_known else None)
        self.output_view.draw(outputs)
        is_complete = self.revealed_count >= len(self.steps)
        self.result_label.configure(text=str(int(np.argmax(outputs))) if is_complete else "?")

        self._show_calculation()
        self.loss_chart.draw(self.loss_history, config.LOSS_HISTORY_STEP)
        last_loss = f"{self.loss_history[-1]:.4f}" if self.loss_history else "–"
        self.training_label.configure(
            text=f"Epoche {self.epoch} von {config.EPOCHS} · Loss {last_loss}"
        )

    def _show_calculation(self) -> None:
        if self.revealed_count >= len(self.steps):
            title = "Alle Knoten berechnet – „Nächster Schritt“ startet die Einzelschritte"
            text = (
                "Jeder Knoten rechnet: gewichtete Summe seiner Eingänge + Bias, "
                "danach die Sigmoid-Funktion σ(z) = 1 / (1 + e^−z)."
            )
        else:
            step = self.steps[self.revealed_count - 1]
            layer = "Hidden-Neuron" if step.layer == HIDDEN_LAYER else "Ausgabe-Neuron"
            source = "Segmente a–g" if step.layer == HIDDEN_LAYER else "Hidden-Neuronen h0–h7"
            title = (
                f"Schritt {self.revealed_count} von {len(self.steps)}: {layer} {step.index} "
                f"(Eingänge: {source})"
            )
            text = step.formula()
        self.step_title.configure(text=title)
        self.calculation.configure(state="normal")
        self.calculation.delete("1.0", "end")
        self.calculation.insert("1.0", text)
        self.calculation.configure(state="disabled")


def main() -> None:
    root = tk.Tk()
    SevenSegmentApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
