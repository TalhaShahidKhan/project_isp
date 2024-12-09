import requests
from decouple import config


BKASH_APP_KEY = config("BKASH_APP_KEY", cast=str)
BKASH_APP_SECRET = config("BKASH_APP_SECRET", cast=str)
BKASH_USERNAME = config("BKASH_USERNAME", cast=str)
BKASH_PASSWORD = config("BKASH_PASSWORD", cast=str)


def create_token(
    bk_username: str = BKASH_USERNAME,
    bk_password: str = BKASH_PASSWORD,
    bk_app: str = BKASH_APP_KEY,
    bk_secret: str = BKASH_APP_SECRET,
):
    url = "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "username": bk_username,
        "password": bk_password,
    }
    body = {
        "app_key": bk_app,
        "app_secret": bk_secret,
    }

    response = requests.post(url=url, headers=headers, json=body)

    return response.json()


def create_payment(
    token,
    amount,
    payer_reference,
    minumber,
    bk_app: str = BKASH_APP_KEY,
    callback: str = "http://127.0.0.1:8000/user_subs/pay",
):
    url = "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/create"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-App-Key": bk_app,
        "Authorization": token,
    }
    body = {
        "amount": amount,
        "mode": "0000",
        "payerReference": payer_reference,
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": minumber,
        "callbackURL": callback,
    }

    response = requests.post(url=url, headers=headers, json=body)

    return response.json()


def exec_payment(paymentId, token, bk_app: str = BKASH_APP_KEY):
    url = "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/execute"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-App-Key": bk_app,
        "Authorization": token,
    }
    body = {"paymentID": paymentId}
    response = requests.post(url=url, headers=headers, json=body)

    return response.json()
