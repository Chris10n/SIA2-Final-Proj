from database.db import init_db
from database.crud import add_user, get_user_by_username


def demo():
    init_db()
    print("\n=== Simple User Database Demo ===")

    while True:
        print("\n[1] Add user")
        print("[2] Get user by username")
        print("[3] Exit")
        choice = input("Select option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            add_user(username, password)

        elif choice == "2":
            username = input("Enter username to search: ")
            user = get_user_by_username(username)
            if user:
                print(f"Username: {user[0]} | Password: {user[1]}")
            else:
                print("User not found.")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    demo()
