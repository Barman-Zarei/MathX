"""Colours for the MathX app: a drafting table at night.

Deep ink-blue paper with a faint graph grid, chalk-white text, and one
accent colour per category that tints the chips, button and answer.
"""
from kivy.utils import get_color_from_hex as _hex

INK = _hex("#0F1128")      # window background
PANEL = _hex("#181B3D")    # inputs and cards
GRID = _hex("#2A2F63")     # graph-paper lines and outlines
CHALK = _hex("#ECEAFF")    # main text
DIM = _hex("#8E92C7")      # secondary text
ERROR = _hex("#FF5D73")

# One accent per category (all light enough for dark text on top).
ACCENTS = {
    "Calculator": _hex("#9B8CFF"),
    "Shapes": _hex("#FFC857"),
    "Circle": _hex("#FF7A90"),
    "Solids": _hex("#5CC8FF"),
    "Trig": _hex("#4FE3B0"),
    "Arithmetic": _hex("#FF9F5A"),
    "Numbers": _hex("#F28CFF"),
    "Algebra": _hex("#B8E35C"),
    "Stats": _hex("#3DD6D0"),
    "Coordinates": _hex("#7C9CFF"),
    "Units": _hex("#FFB199"),
    "Formulas": _hex("#E8D26B"),
}
