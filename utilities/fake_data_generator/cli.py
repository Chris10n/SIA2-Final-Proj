import argparse
import json
from generator import FakeDataGenerator


def main():
    p = argparse.ArgumentParser(description="Generate fake data to stdout or file")
    p.add_argument("-n", "--number", type=int, default=10, help="number of records")
    p.add_argument("-o", "--outfile", default=None, help="output file (json). If omitted, prints to stdout")
    p.add_argument("--locale", default=None, help="Faker locale, e.g. en_US")
    p.add_argument("--seed", type=int, default=None, help="optional seed for reproducibility")
    args = p.parse_args()

    g = FakeDataGenerator(locale=args.locale, seed=args.seed)
    data = g.generate(args.number)
    if args.outfile:
        with open(args.outfile, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"Wrote {len(data)} records to {args.outfile}")
    else:
        print(json.dumps(data, indent=2, default=str))


if __name__ == "__main__":
    main()
