import json
from .generator import generate_fake_people


def _main() -> None:
    people = generate_fake_people(3, seed=42)
    print(json.dumps(people, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _main()
