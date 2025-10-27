import validate as v
import encryption as e


def main():
    password = "HelloWorld"
    hashedPassword = e.hash_password(password)
    print(f"Valid Password: {v.is_valid_password(password)}")
    print(f"Hashed Password: {hashedPassword}")
    print(f"Password Verify: {e.verify_password(hashedPassword, password)}")


if __name__ == "__main__":
    main()
