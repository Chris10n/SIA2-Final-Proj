from faker import Faker
from typing import List, Dict, Any, Optional


class FakeDataGenerator:
    """Lightweight wrapper around Faker. No authentication here — keep logic
    separate so GUI/auth can be implemented elsewhere."""

    def __init__(self, locale: Optional[str] = None, seed: Optional[int] = None):
        self._faker = Faker(locale) if locale else Faker()
        if seed is not None:
            self._faker.seed_instance(seed)

    def _single(self) -> Dict[str, Any]:
        return {
            "name": self._faker.name(),
            "address": self._faker.address(),
            "email": self._faker.email(),
            "phone_number": (
                self._faker.phone_number()
                if hasattr(self._faker, "phone_number")
                else self._faker.numerify("09#########")
            ),
            "company": self._faker.company(),
            "job": self._faker.job(),
            "date_of_birth": self._faker.date_of_birth().isoformat(),
        }

    def generate(self, n: int = 10) -> List[Dict[str, Any]]:
        if n <= 0:
            return []
        return [self._single() for _ in range(int(n))]


