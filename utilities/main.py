"""Utilities entrypoint for the fake data generator package.

Run either the temporary GUI or generate data from the command line.

Examples:
  python -m utilities.main gui
  python -m utilities.main generate -n 10 --locale en_PH
"""
from __future__ import annotations

import argparse
import json
from typing import Optional

from utilities.fake_data_generator import FakeDataGenerator, open_fake_data_gui


def _cmd_gui() -> None:
    open_fake_data_gui()


def _cmd_generate(n: int = 10, locale: Optional[str] = None, seed: Optional[int] = None) -> None:
    gen = FakeDataGenerator(locale=locale, seed=seed)
    data = gen.generate(n)
    print(json.dumps(data, indent=2, default=str))


def main() -> None:
    parser = argparse.ArgumentParser(description="Utilities: fake data generator")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("gui", help="Open temporary Tkinter GUI (optional)")

    gen_p = sub.add_parser("generate", help="Generate fake data from CLI")
    gen_p.add_argument("-n", "--number", type=int, default=10, help="Number of records")
    gen_p.add_argument("--locale", type=str, default=None, help="Faker locale (e.g. en_PH)")
    gen_p.add_argument("--seed", type=int, default=None, help="Optional integer seed")

    args = parser.parse_args()

    if args.command == "gui":
        _cmd_gui()
    elif args.command == "generate":
        _cmd_generate(args.number, args.locale, args.seed)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
