from faker import Faker
from typing import List, Dict, Any, Optional


class FakeDataGenerator:
    """Simple wrapper around Faker to generate consistent records.

    Usage:
        g = FakeDataGenerator(locale='en_US', seed=42)
        data = g.generate(100)
    """

    def __init__(self, locale: Optional[str] = None, seed: Optional[int] = None):
        self.locale = locale
        self.seed = seed
        # Initialize Faker instance
        self._faker = Faker(locale) if locale else Faker()
        if seed is not None:
            self._faker.seed_instance(seed)

    def _single(self) -> Dict[str, Any]:
        """Generate a single synthetic record."""
        return {
            "name": self._faker.name(),
            "address": self._faker.address(),
            "email": self._faker.email(),
            # Some locales (eg. certain PH locales) may not expose phone_number.
            # Use a fallback pattern for Philippine mobile numbers if provider missing.
            "phone_number": (self._faker.phone_number()
                             if hasattr(self._faker, "phone_number")
                             else self._faker.numerify("09#########")),
            "company": self._faker.company(),
            "job": self._faker.job(),
            "date_of_birth": self._faker.date_of_birth().isoformat(),
        }

    def generate(self, n: int = 10) -> List[Dict[str, Any]]:
        """Generate n records.

        Args:
            n: number of records to generate
        Returns:
            list of dict records
        """
        if n <= 0:
            return []
        return [self._single() for _ in range(int(n))]
