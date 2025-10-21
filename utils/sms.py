from requests import post
from json import dumps
from re import match
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def __is_valid_number(number: str) -> bool:
    patternE164 = r"^\+[1-9]\d{1,14}$"

    try:
        if len(number) > 16:
            raise Exception("Number is too long.")
        if not bool(match(patternE164, number)):
            raise Exception("Number does not adhere to E.164 format.")
    except Exception as e:
        print(f"Invalid phone number: {e}")
        return False

    return True


def __is_valid_message(message: str) -> bool:
    try:
        if len(message.strip()) > 160:
            raise Exception("Message exceeds max cap of 160.")
    except Exception as e:
        print(f"Invalid message: {e}")
        return False

    return True


def send_SMS(recipient: str, message: str):
    if not __is_valid_number(recipient):
        return

    if not __is_valid_message(message):
        return

    apiKey = getenv("HTTPSMS_API_KEY")
    url = "https://api.httpsms.com/v1/messages/send"

    headers = {
        "x-api-key": apiKey,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "content": message,
        "from": getenv("SMS_GATEWAY"),
        "to": recipient,
    }

    response = post(url, headers=headers, data=dumps(payload))
    print(dumps(response.json(), indent=4))
