from sms import send_SMS


def main():
    print("Send an SMS")
    recipient = input("Input recipient number [ex: +639123456789]: ").strip()
    message = input("Input your message: ")

    send_SMS(recipient, message)


if __name__ == "__main__":
    main()
