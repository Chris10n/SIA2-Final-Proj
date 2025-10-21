from faker import Faker
from typing import Optional, List, Dict, Any


def generate_fake_people(
    numOfRecords: int = 10, *, locale: Optional[str] = None, seed: Optional[int] = None
) -> List[Dict[str, Any]]:
    fake = Faker(locale) if locale else Faker()
    if seed is not None:
        fake.seed_instance(seed)

    people: List[Dict[str, Any]] = []
    for _ in range(numOfRecords):
        people.append(
            {
                "name": fake.name(),
                "address": fake.address().replace("\n", ", "),
                "email": fake.email(),
                "phone_number": fake.numerify("09#########"),
                "company": fake.company(),
                "job": fake.job(),
                "date_of_birth": fake.date_of_birth().isoformat(),
            }
        )
    return people
