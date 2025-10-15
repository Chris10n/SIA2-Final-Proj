# Fake Data Generator

Modular fake-data generator using Faker. The codebase keeps the generator
logic separate from the temporary GUI so the GUI can be removed later
without affecting the core functionality.

Structure
---------

utilities/
└── fake_data_generator/
	├── generator.py   # pure data logic (FakeDataGenerator)
	├── cli.py         # small CLI wrapper
	├── gui.py         # temporary Tkinter GUI (optional)
	└── __init__.py

How to use
----------

Programmatically:

from utilities.fake_data_generator import FakeDataGenerator

g = FakeDataGenerator(locale='en_US', seed=42)
data = g.generate(10)

CLI (module form):

python -m utilities.fake_data_generator.cli -n 10

GUI (temporary):

python -m utilities.fake_data_generator.gui

Dependencies
------------

See `requirements.txt` (Faker). Use a virtual environment for development.
