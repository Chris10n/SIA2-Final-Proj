from json import dumps
from utils.url_shortener import shorten_tinyurl
from utils.sms import send_SMS
from utils.generator import generate_fake_people

# For Testing Purposes Only


def main():
    divider = "=" * 25
    RUNNING = True

    while RUNNING:
        print("Utilities Test CLI")
        print(divider)
        print("1. URL Shortener")
        print("2. SMS & Messaging")
        print("3. Fake Data Generator")
        print("4. Exit")
        print(divider)
        userInput = int(input("Choose an option [1, 2, 3, 4]: ").strip())

        match userInput:
            case 1:
                shorten_url()
            case 2:
                sms()
            case 3:
                generate_fake_data()
            case 4:
                print("Thank you, shutting down...")
                RUNNING = False
            case _:
                print("Invalid input, try again.")
        print(divider)


def shorten_url():
    url = input("Input URL to shorten: ").strip()
    shortenedUrl = shorten_tinyurl(url)
    print(shortenedUrl)


def sms():
    recipient = input(
        "Input recipient number in E.164 format (Ex: +639123456789): "
    ).strip()
    message = input("Input message: ").strip()
    send_SMS(recipient, message)


def generate_fake_data():
    numberOfRecords = int(input("Enter number of desired records: ").strip())
    fakeData = generate_fake_people(numberOfRecords)
    print(dumps(fakeData, indent=4))


if __name__ == "__main__":
    main()
