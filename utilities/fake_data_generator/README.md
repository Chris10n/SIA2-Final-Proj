# Fake Data Generator

Small utility wrapping Faker to produce previewable datasets and export to CSV/JSON.

Usage
-----

Programmatically

from generator import FakeDataGenerator

g = FakeDataGenerator(locale='en_US', seed=42)
data = g.generate(100)

GUI
---

Run:

python gui.py

Click "Generate Preview" then export as CSV or JSON.

CLI
---

Run:

python cli.py -n 50 -o sample50.json

Dependencies
------------

See `requirements.txt`.
