from faker import Faker
from typing import List, Dict, Any, Optional
import json
from typing import Callable, TYPE_CHECKING
import importlib


class AuthenticationError(PermissionError):
    """Raised when authentication fails."""


class FakeDataGenerator:
    """Simple wrapper around Faker to generate consistent records.

    Usage:
        g = FakeDataGenerator(locale='en_US', seed=42)
        data = g.generate(100)
    """

    def __init__(self, locale: Optional[str] = None, seed: Optional[int] = None,
                 username: Optional[str] = None, password: Optional[str] = None,
                 authenticated_user: Optional[str] = None):
        self.locale = locale
        self.seed = seed
        # Optional authentication context. The generator will attempt to verify
        # credentials if username/password are supplied. If `authenticated_user`
        # is provided we assume a prior successful login and skip verification.
        self._username = username
        self._password = password
        self._authenticated_user = authenticated_user

        # Initialize Faker instance
        self._faker = Faker(locale) if locale else Faker()
        if seed is not None:
            self._faker.seed_instance(seed)
        # perform credential verification lazily on generate() to avoid
        # importing auth modules at top-level during packaging.
        self._auth_checked = False

    def _check_auth(self) -> bool:
        """Return True if the user is authenticated.

        If username/password were supplied, call into the auth package to
        verify them. If authenticated_user is provided, accept as authenticated.
        """
        if self._auth_checked:
            return True
        if self._authenticated_user:
            self._auth_checked = True
            return True
        if not self._username:
            # no credentials provided; treat as unauthenticated but allow
            # generation (backwards-compatible). Caller can opt to require auth.
            return False
        # lazy import using importlib so static analyzers (Pylance) don't
        # report missing imports while preserving runtime lazy-import behavior.
        if TYPE_CHECKING:
            # For type checkers only: this path isn't executed at runtime but
            # helps tools resolve the symbol.
            from auth.user_auth import verify_user  # type: ignore

        try:
            mod = importlib.import_module("auth.user_auth")
            verify_user = getattr(mod, "verify_user")
        except Exception:
            # If auth package is missing at runtime, raise a clear error.
            raise AuthenticationError("Authentication module not available")

        ok = verify_user(self._username, self._password or "")
        if not ok:
            raise AuthenticationError("Invalid username or password")
        self._auth_checked = True
        return True

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
        # check authentication; if credentials were provided, this will raise
        # AuthenticationError on failure. If no credentials were provided this
        # will return False but we still allow generation for backwards
        # compatibility.
        try:
            self._check_auth()
        except AuthenticationError:
            # re-raise to caller
            raise

        return [self._single() for _ in range(int(n))]


