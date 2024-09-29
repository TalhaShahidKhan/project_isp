import requests
from decouple import config

base_url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/"

BKASH_APP_KEY = config("BKASH_APP_KEY", cast=str)
BKASH_APP_SECRET = config("BKASH_APP_SECRET", cast=str)
BKASH_USERNAME = config("BKASH_USERNAME", cast=str)
BKASH_PASSWORD = config("BKASH_PASSWORD", cast=str)


def create_token():
    url = f"{base_url}tokenized/checkout/token/grant"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "username": BKASH_USERNAME,
        "password": BKASH_PASSWORD,
    }
    body = {
        "app_key": BKASH_APP_KEY,
        "app_secret": BKASH_APP_SECRET,
    }

    response = requests.post(url=url, headers=headers, json=body)

    return response.json()


def create_payment(
    token,
    amount,
    payer_reference,
    minumber,
):
    url = f"{base_url}tokenized/checkout/create"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-App-Key": BKASH_APP_KEY,
        "Authorization": token,
    }
    body = {
        "amount": amount,
        "mode": "0000",
        "payerReference": payer_reference,
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": minumber,
        "callbackURL": "http://127.0.0.1:8000/user_subs/pay",
    }

    response = requests.post(url=url, headers=headers, json=body)

    return response.json()


def exec_payment(paymentId, token):
    url = f"{base_url}tokenized/checkout/execute"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-App-Key": BKASH_APP_KEY,
        "Authorization": token,
    }
    body = {"paymentID": paymentId}
    response = requests.post(url=url, headers=headers, json=body)

    return response.json()
