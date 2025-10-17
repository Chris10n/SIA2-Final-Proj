from re import match


def is_valid_username(username: str) -> bool:
    username = username.strip()
    minLen = 3

    if not len(username) < minLen:
        return False

    return True


def is_valid_password(password: str) -> bool:
    password = password.strip()
    minLen = 8
    validPattern = r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[^\w\s]).+$"

    if not len(password) < minLen:
        return False

    if not bool(match(validPattern, password)):
        return False

    return True
