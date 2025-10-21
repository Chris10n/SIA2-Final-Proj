import json
from generator import generate_fake_people


def _main() -> None:
    numOfRecords = int(input("Enter desired number of records: ").strip())
    people = generate_fake_people(numOfRecords, seed=42)
    print(json.dumps(people, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _main()
