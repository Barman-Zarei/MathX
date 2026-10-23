"""MathX desktop/mobile app (Kivy).

Run from the project root:

    pip install -e lib
    pip install -r script/requirements.txt
    python script/main.py
"""
import math
import os
import sys

# Make `tools` and `theme` importable no matter where the app is started from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.config import Config  # noqa: E402

Config.set("graphics", "width", "460")
Config.set("graphics", "height", "780")
Config.set("graphics", "minimum_width", "340")
Config.set("graphics", "minimum_height", "560")
Config.set("input", "mouse", "mouse,disable_multitouch")

import mathx  # noqa: E402
import theme as T  # noqa: E402
import tools  # noqa: E402
from kivy.animation import Animation  # noqa: E402
from kivy.app import App  # noqa: E402
from kivy.clock import Clock  # noqa: E402
from kivy.core.window import Window  # noqa: E402
from kivy.graphics import Color, Line  # noqa: E402
from kivy.lang import Builder  # noqa: E402
from kivy.metrics import dp, sp  # noqa: E402
from kivy.properties import ListProperty, NumericProperty, StringProperty  # noqa: E402
from kivy.uix.boxlayout import BoxLayout  # noqa: E402
from kivy.uix.button import Button  # noqa: E402
from kivy.uix.floatlayout import FloatLayout  # noqa: E402
from kivy.uix.gridlayout import GridLayout  # noqa: E402
from kivy.uix.label import Label  # noqa: E402
from kivy.uix.scrollview import ScrollView  # noqa: E402
from kivy.uix.textinput import TextInput  # noqa: E402
from kivy.uix.togglebutton import ToggleButton  # noqa: E402
from kivy.uix.widget import Widget  # noqa: E402

KV = """
#:import T theme
#:import dp kivy.metrics.dp
#:import sp kivy.metrics.sp

<Chip>:
    background_normal: ''
    background_down: ''
    background_color: 0, 0, 0, 0
    color: T.CHALK if self.state == 'normal' else T.INK
    bold: self.state == 'down'
    font_size: sp(15)
    size_hint: None, None
    height: dp(40)
    width: self.texture_size[0] + dp(30)
    canvas.before:
        Color:
            rgba: T.PANEL if self.state == 'normal' else self.accent
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(20)]
    canvas.after:
        Color:
            rgba: T.GRID if self.state == 'normal' else (0, 0, 0, 0)
        Line:
            rounded_rectangle: self.x, self.y, self.width, self.height, dp(20)
            width: 1

<FieldInput>:
    multiline: False
    write_tab: False
    background_normal: ''
    background_active: ''
    background_disabled_normal: ''
    background_color: 0, 0, 0, 0
    foreground_color: T.CHALK
    hint_text_color: T.DIM
    cursor_color: app.accent
    selection_color: app.accent[0], app.accent[1], app.accent[2], 0.35
    font_size: sp(18)
    padding: dp(14), max((self.height - self.line_height) / 2, 0)
    size_hint_y: None
    height: dp(50)
    canvas.before:
        Color:
            rgba: T.PANEL
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12)]
        Color:
            rgba: app.accent if self.focus else T.GRID
        Line:
            rounded_rectangle: self.x, self.y, self.width, self.height, dp(12)
            width: dp(1.4) if self.focus else 1
        Color:
            rgba: 1, 1, 1, 1

<CalcButton>:
    background_normal: ''
    background_down: ''
    background_color: 0, 0, 0, 0
    color: T.INK
    bold: True
    font_size: sp(18)
    size_hint_y: None
    height: dp(54)
    canvas.before:
        Color:
            rgba: (app.accent[0] * .8, app.accent[1] * .8, app.accent[2] * .8, 1) if self.state == 'down' else app.accent
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(14)]

<ResultCard>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    padding: dp(20), dp(12), dp(14), dp(14)
    spacing: dp(2)
    canvas.before:
        Color:
            rgba: T.PANEL
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(14)]
        Color:
            rgba: T.DIM if self.kind == 'idle' else (T.ERROR if self.kind == 'error' else app.accent)
        RoundedRectangle:
            pos: self.x + dp(8), self.y + dp(12)
            size: dp(4), max(self.height - dp(24), 0)
            radius: [dp(2)]
    Label:
        text: root.title
        color: T.DIM
        font_size: sp(13)
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        halign: 'left'
    Label:
        text: root.main
        color: T.DIM if root.kind == 'idle' else (T.ERROR if root.kind == 'error' else app.accent)
        font_size: sp(30) if root.kind == 'ok' else sp(16)
        bold: root.kind == 'ok'
        size_hint_y: None
        height: self.texture_size[1] + dp(6)
        text_size: self.width, None
        halign: 'left'
        valign: 'middle'
    Label:
        text: root.detail
        color: T.DIM
        font_size: sp(14)
        size_hint_y: None
        height: self.texture_size[1] if root.detail else 0
        opacity: 1 if root.detail else 0
        text_size: self.width, None
        halign: 'left'
"""


class Chip(ToggleButton):
    accent = ListProperty(T.ACCENTS["Calculator"])


class FieldInput(TextInput):
    pass


class CalcButton(Button):
    pass


class ResultCard(BoxLayout):
    kind = StringProperty("idle")  # idle | ok | error
    title = StringProperty("Answer")
    main = StringProperty("Pick a tool, fill in the numbers, press Calculate.")
    detail = StringProperty("")


class Backdrop(FloatLayout):
    """Ink-blue paper with a faint graph grid."""

    STEP = dp(28)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._draw, pos=self._draw)

    def _draw(self, *_):
        self.canvas.before.clear()
        w, h = self.size
        with self.canvas.before:
            Color(*T.INK)
            from kivy.graphics import Rectangle

            Rectangle(pos=self.pos, size=self.size)
            n = 0
            x = self.x
            while x <= self.right:
                Color(*T.GRID[:3], 0.55 if n % 4 == 0 else 0.22)
                Line(points=[x, self.y, x, self.top], width=1)
                x += self.STEP
                n += 1
            n = 0
            y = self.y
            while y <= self.top:
                Color(*T.GRID[:3], 0.55 if n % 4 == 0 else 0.22)
                Line(points=[self.x, y, self.right, y], width=1)
                y += self.STEP
                n += 1


class WaveHeader(Widget):
    """A sine and cosine pair drifting across the header (sine takes the accent colour)."""

    phase = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(*T.GRID)
            self._axis = Line(points=[], width=1)
            self._cos_color = Color(*T.DIM[:3], 0.6)
            self._cos = Line(points=[], width=dp(1.6))
            self._sin_color = Color(*T.ACCENTS["Calculator"])
            self._sin = Line(points=[], width=dp(2.4))
        self.bind(size=self._redraw, pos=self._redraw)
        Clock.schedule_interval(self._tick, 1 / 30)

    def set_accent(self, rgba):
        self._sin_color.rgba = rgba

    def _tick(self, dt):
        self.phase += dt * 1.2
        self._redraw()

    def _redraw(self, *_):
        w, h = self.size
        if w <= 0 or h <= 0:
            return
        mid = self.y + h / 2
        amp = h * 0.32
        sin_pts, cos_pts = [], []
        steps = 64
        for i in range(steps + 1):
            u = i / steps
            x = self.x + w * u
            t = u * 2 * math.pi * 1.4 + self.phase
            sin_pts += [x, mid + amp * math.sin(t)]
            cos_pts += [x, mid + amp * 0.7 * math.cos(t)]
        self._axis.points = [self.x, mid, self.right, mid]
        self._sin.points = sin_pts
        self._cos.points = cos_pts


class ChipRow(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(
            do_scroll_x=True, do_scroll_y=False, bar_width=0,
            size_hint_y=None, height=dp(48), **kwargs,
        )
        self.box = GridLayout(
            rows=1, size_hint_x=None, spacing=dp(8), padding=(dp(14), dp(4)),
        )
        self.box.bind(minimum_width=self.box.setter("width"))
        self.add_widget(self.box)

    def clear(self):
        self.box.clear_widgets()

    def add(self, chip):
        self.box.add_widget(chip)


class MathXApp(App):
    title = "MathX"
    accent = ListProperty(T.ACCENTS["Calculator"])

    def build(self):
        Window.clearcolor = T.INK
        Window.softinput_mode = "below_target"
        Builder.load_string(KV)
        self.category = None
        self.tool = None
        self.inputs = {}

        root = Backdrop()
        col = BoxLayout(orientation="vertical", padding=(0, dp(10), 0, dp(12)), spacing=dp(6))

        header = BoxLayout(size_hint_y=None, height=dp(84), padding=(dp(20), 0, dp(12), 0))
        left = BoxLayout(orientation="vertical", size_hint_x=0.5)
        logo = Label(
            text="[b]Math[/b][b][color=ffc857]X[/color][/b]", markup=True, font_size=sp(42),
            halign="left", valign="bottom", color=T.CHALK,
        )
        logo.bind(size=lambda w, s: setattr(w, "text_size", s))
        sub = Label(
            text=f"mathx {mathx.__version__}", font_size=sp(13), color=T.DIM,
            halign="left", valign="top", size_hint_y=None, height=dp(20),
        )
        sub.bind(size=lambda w, s: setattr(w, "text_size", s))
        left.add_widget(logo)
        left.add_widget(sub)
        header.add_widget(left)
        self.wave = WaveHeader()
        self.bind(accent=lambda inst, value: self.wave.set_accent(value))
        header.add_widget(self.wave)
        col.add_widget(header)

        self.cat_row = ChipRow()
        self.tool_row = ChipRow()
        col.add_widget(self.cat_row)
        col.add_widget(self.tool_row)

        self.note = Label(
            text="", font_size=sp(13), color=T.DIM, size_hint_y=None, height=dp(24),
            halign="left", valign="middle",
        )
        self.note.bind(size=lambda w, s: setattr(w, "text_size", (s[0] - dp(40), s[1])))
        col.add_widget(self.note)

        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3), bar_color=T.GRID)
        self.form = GridLayout(
            cols=1, size_hint_y=None, spacing=dp(6), padding=(dp(18), dp(4), dp(18), dp(8)),
        )
        self.form.bind(minimum_height=self.form.setter("height"))
        scroll.add_widget(self.form)
        col.add_widget(scroll)

        bottom = BoxLayout(
            orientation="vertical", size_hint_y=None, spacing=dp(10), padding=(dp(18), 0),
        )
        bottom.bind(minimum_height=bottom.setter("height"))
        self.calc = CalcButton(text="Calculate")
        self.calc.bind(on_release=lambda *_: self.calculate())
        self.card = ResultCard()
        bottom.add_widget(self.calc)
        bottom.add_widget(self.card)
        col.add_widget(bottom)

        root.add_widget(col)

        first = None
        for name in tools.CATEGORIES:
            chip = Chip(text=name, group="category", allow_no_selection=False)
            chip.accent = T.ACCENTS[name]
            chip.bind(state=lambda w, s, n=name: s == "down" and self.select_category(n))
            self.cat_row.add(chip)
            first = first or chip
        first.state = "down"
        return root

    # ------------------------------------------------------------ selection

    def select_category(self, name):
        self.category = name
        target = T.ACCENTS[name]
        Animation(accent=target, duration=0.25, t="out_quad").start(self)
        self.tool_row.clear()
        first = None
        for t in tools.CATEGORIES[name]:
            chip = Chip(text=t.title, group="tool", allow_no_selection=False)
            chip.accent = target
            chip.bind(state=lambda w, s, tl=t: s == "down" and self.select_tool(tl))
            self.tool_row.add(chip)
            first = first or chip
        self.tool_row.scroll_x = 0
        first.state = "down"

    def select_tool(self, tool):
        self.tool = tool
        self.inputs = {}
        self.note.text = tool.note
        self.form.clear_widgets()
        text_inputs = []
        for field in tool.fields:
            if field.kind == "bool":
                chip = Chip(text=field.label)
                chip.accent = T.ACCENTS[self.category]
                self.form.add_widget(chip)
                self.inputs[field.key] = chip
                continue
            label = Label(
                text=field.label, font_size=sp(13), color=T.DIM, size_hint_y=None,
                height=dp(22), halign="left", valign="bottom",
            )
            label.bind(size=lambda w, s: setattr(w, "text_size", s))
            box = FieldInput(hint_text=field.hint)
            self.form.add_widget(label)
            self.form.add_widget(box)
            self.inputs[field.key] = box
            text_inputs.append(box)
        for i, box in enumerate(text_inputs):
            if i + 1 < len(text_inputs):
                box.bind(on_text_validate=lambda w, nxt=text_inputs[i + 1]: setattr(nxt, "focus", True))
            else:
                box.bind(on_text_validate=lambda *_: self.calculate())
        if text_inputs:
            Clock.schedule_once(lambda dt: setattr(text_inputs[0], "focus", True), 0.05)
        self.card.kind = "idle"
        self.card.title = "Answer"
        self.card.main = "Fill in the fields and press Calculate."
        self.card.detail = ""

    # ----------------------------------------------------------- calculate

    def calculate(self):
        raw = {}
        for key, widget in self.inputs.items():
            raw[key] = widget.state == "down" if isinstance(widget, Chip) else widget.text
        try:
            main, detail = tools.run_tool(self.tool, raw)
            kind = "ok"
        except (ValueError, TypeError, OverflowError, ZeroDivisionError) as exc:
            main, detail, kind = str(exc) or "That input did not work.", "", "error"
        except Exception as exc:  # keep the app alive whatever happens
            main, detail, kind = f"Unexpected problem: {exc}", "", "error"
        self.card.kind = kind
        self.card.title = self.tool.title if kind == "ok" else "Check your input"
        self.card.main = main
        self.card.detail = detail
        self.card.opacity = 0
        Animation(opacity=1, duration=0.2).start(self.card)

    def on_pause(self):
        return True


if __name__ == "__main__":
    MathXApp().run()
