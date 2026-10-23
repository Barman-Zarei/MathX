# MathX

A maths toolkit in two parts:

| Folder | What it is |
| --- | --- |
| lib/ | The mathx Python package (published on PyPI as mathzx): pure functions, no dependencies, Python 3.8+. |
| script/ | A Kivy app (desktop or mobile) that uses mathx through a graphical interface. |


MathX/
├── lib/
│   ├── mathx/            the package (circle, shapes/, trig, arithmetic, number_theory,
│   │                     algebra, stats, coordinate, units, formulas, expression)
│   ├── tests/            pytest tests
│   ├── pyproject.toml
│   ├── README.md
│   ├── CHANGELOG.md
│   └── LICENSE
├── script/
│   ├── main.py           the Kivy app (look, layout, animation)
│   ├── tools.py          which tools exist, input parsing, answer formatting (no Kivy)
│   ├── theme.py          colours
│   ├── tests/
│   └── requirements.txt
├── LICENSE
└── .gitignore


## Run the app

bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e lib
pip install -r script/requirements.txt
python script/main.py


## Develop and test the library

bash
pip install -e "lib[dev]"
cd lib && pytest && ruff check .


App logic tests (no Kivy window needed): cd script && pytest tests.

## Publish the library

bash
cd lib
pip install build twine
python -m build
twine check dist/*
twine upload --repository testpypi dist/*   # try it first
twine upload dist/*


The PyPI package name is mathzx (set in lib/pyproject.toml); the import name stays mathx:

bash
pip install mathzx

python
import mathx


## License

MIT (c) Barman
