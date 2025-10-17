from faker import Faker
import random
from typing import Optional, List, Dict, Any
from faker import Faker


def generate_fake_people(n: int = 10, *, locale: Optional[str] = None, seed: Optional[int] = None) -> List[Dict[str, Any]]:
    """Return a list of n fake person-like records.

    Args:
        n: number of records to generate.
        locale: optional Faker locale (e.g. "en_US", "en_PH").
        seed: optional integer seed to make results deterministic.

    Returns:
        List of dicts with keys: name, address, email, phone_number, company, job, date_of_birth.
    """

    fake = Faker(locale) if locale else Faker()
    if seed is not None:
        # make this instance deterministic
        fake.seed_instance(seed)

    people: List[Dict[str, Any]] = []
    for _ in range(n):
        people.append({
            "name": fake.name(),
            "address": fake.address().replace("\n", ", "),
            "email": fake.email(),
            "phone_number": fake.numerify("09#########"),
            "company": fake.company(),
            "job": fake.job(),
            "date_of_birth": fake.date_of_birth().isoformat(),
        })
    return people


if __name__ == "__main__":
    # quick smoke-run
    for person in generate_fake_people(5):
        print(person)
