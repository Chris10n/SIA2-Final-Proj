import requests
import json
from os import getenv
from sys import exit
from dotenv import load_dotenv

load_dotenv()


def __validate_number(number: str):
    try:
        if len(number) > 13:
            raise Exception("Recipient number is too long.")
    except Exception as e:
        print(f"Invalid phone number: {e}")
        exit(1)


def send_SMS(recipient: str, message: str):
    __validate_number(recipient)

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

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(json.dumps(response.json(), indent=4))
