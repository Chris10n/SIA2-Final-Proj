import argparse
import json
import os
import sys
from ..utilities.fake_data_generator.generator import FakeDataGenerator


def main():
    p = argparse.ArgumentParser(description="Generate fake data to stdout")
    p.add_argument("-n", "--number", type=int, default=10, help="number of records")
    p.add_argument("--locale", default=None, help="Faker locale, e.g. en_US")
    p.add_argument("--seed", type=int, default=None, help="optional seed for reproducibility")
    args = p.parse_args()

    g = FakeDataGenerator(locale=args.locale, seed=args.seed)
    data = g.generate(args.number)

    print(json.dumps(data, indent=2, default=str))


if __name__ == "__main__":
    main()
