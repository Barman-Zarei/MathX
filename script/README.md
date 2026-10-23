# MathX app

A Kivy front end for the `mathx` library.

- Twelve categories (Calculator, Shapes, Circle, Solids, Trig, Arithmetic, Numbers, Algebra,
  Stats, Coordinates, Units, Formulas), each with its own accent colour.
- Number fields accept expressions: `pi/2`, `3*4`, `2^10`.
- Lists use commas or spaces (`2, 4, 4, 5`), points use `x, y`, and several points or matrix
  rows are separated by `;` (`0,0; 4,0; 4,3`).
- Enter jumps to the next field and calculates on the last one.

## Run

From the project root:

    pip install -e lib
    pip install -r script/requirements.txt
    python script/main.py

## Where to change things

- `tools.py`: add a tool by adding one `tool(...)` line to `CATEGORIES`. The field `key`
  must match the function's parameter name.
- `theme.py`: colours. `main.py`: layout and animation.
