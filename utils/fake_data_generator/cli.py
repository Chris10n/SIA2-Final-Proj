import argparse
import json
import os
import sys
from generator import FakeDataGenerator


def main():
    p = argparse.ArgumentParser(description="Generate fake data to stdout or file")
    p.add_argument("-n", "--number", type=int, default=10, help="number of records")
    p.add_argument(
        "-o",
        "--outfile",
        default=None,
        help="output file (json). If omitted, prints to stdout",
    )
    p.add_argument(
        "--force", action="store_true", help="overwrite outfile if it exists"
    )
    p.add_argument("--locale", default=None, help="Faker locale, e.g. en_US")
    p.add_argument(
        "--seed", type=int, default=None, help="optional seed for reproducibility"
    )
    # authentication handled outside of generator; CLI remains simple
    args = p.parse_args()

    g = FakeDataGenerator(locale=args.locale, seed=args.seed)
    data = g.generate(args.number)

    if args.outfile:
        if args.number < 0:
            print("--number must be >= 0")
            raise SystemExit(2)

        out_dir = os.path.dirname(os.path.abspath(args.outfile))
        if out_dir and not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir, exist_ok=True)
            except OSError as e:
                print(f"Could not create directory {out_dir}: {e}")
                raise SystemExit(1)

        if os.path.exists(args.outfile) and not args.force:
            print(f"Error: '{args.outfile}' already exists. Use --force to overwrite.")
            raise SystemExit(2)

        try:
            with open(args.outfile, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except OSError as e:
            print(f"Error writing to {args.outfile}: {e}")
            raise SystemExit(1)

        print(f"Wrote {len(data)} records to {args.outfile}")
    else:
        print(json.dumps(data, indent=2, default=str))


if __name__ == "__main__":
    main()
