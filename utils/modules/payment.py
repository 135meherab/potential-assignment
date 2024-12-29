import json

import requests
from django.conf import settings

from utils.helper import string_to_base64


class AuthorizeNet:
    def __init__(self, api_login_id, transaction_key):
        self.api_login_id = api_login_id
        self.transaction_key = transaction_key

    def _get_merchant_auth(self):
        merchant_auth = {
            "name": self.api_login_id,
            "transactionKey": self.transaction_key,
        }
        return merchant_auth

    @staticmethod
    def _get_credit_card(card_number, card_expiry, card_cvc=None):
        credit_card = {
            "cardNumber": card_number,
            "expirationDate": card_expiry,
        }
        if card_cvc:
            credit_card["cardCode"] = card_cvc
        return credit_card

    @staticmethod
    def _get_customer_address(
        first_name, last_name, company, address, city, state, zipcode, country
    ):
        customer_address = {
            "firstName": first_name,
            "lastName": last_name,
            "company": company,
            "address": address,
            "city": city,
            "state": state,
            "zip": zipcode,
            "country": country,
        }
        return customer_address

    @staticmethod
    def _get_customer_data(user):
        customer_data = {"type": "individual", "id": user.username, "email": user.email}
        return customer_data

    def charge_credit_card(
        self,
        card_number,
        card_expiry,
        card_cvc,
        amount,
        first_name,
        last_name,
        company,
        address,
        city,
        state,
        zipcode,
        country,
        user,
        is_save_card=False,
    ):
        merchant_auth = self._get_merchant_auth()
        credit_card = self._get_credit_card(card_number, card_expiry, card_cvc)
        customer_address = self._get_customer_address(
            first_name, last_name, company, address, city, state, zipcode, country
        )
        # customer_data = self._get_customer_data(user)

        payload = {
            "createTransactionRequest": {
                "merchantAuthentication": merchant_auth,
                # "refId": "MerchantID-0001",
                "transactionRequest": {
                    "transactionType": "authCaptureTransaction",
                    "amount": str(amount),
                    "payment": {"creditCard": credit_card},
                    "billTo": customer_address,
                    # "customer": customer_data
                },
            }
        }

        response = requests.post(
            settings.AUTHORIZE_NET_TRANSACTION_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

        response_data = json.loads(response.content.decode("utf-8-sig"))

        if is_save_card:
            if (
                authorizenet_customer_profile_id := user.user_information.authorizenet_customer_profile_id
            ):
                self.create_customer_payment_profile(
                    card_number,
                    card_expiry,
                    authorizenet_customer_profile_id,
                    customer_address,
                )

            else:
                self.create_customer_profile(
                    card_number, card_expiry, user, customer_address
                )

        return response_data

    def charge_customer_profile(self, user, customer_payment_profile_id, amount):
        merchant_auth = self._get_merchant_auth()

        payload = {
            "createTransactionRequest": {
                "merchantAuthentication": merchant_auth,
                "transactionRequest": {
                    "transactionType": "authCaptureTransaction",
                    "amount": str(amount),
                    "profile": {
                        "customerProfileId": user.user_information.authorizenet_customer_profile_id,
                        "paymentProfile": {
                            "paymentProfileId": customer_payment_profile_id
                        },
                    },
                },
            }
        }

        response = requests.post(
            settings.AUTHORIZE_NET_TRANSACTION_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

        response_data = json.loads(response.content.decode("utf-8-sig"))

        return response_data

    def create_customer_payment_profile(
        self,
        card_number,
        card_expiry,
        authorizenet_customer_profile_id,
        customer_address,
    ):
        merchant_auth = self._get_merchant_auth()

        payload = {
            "createCustomerPaymentProfileRequest": {
                "merchantAuthentication": merchant_auth,
                "customerProfileId": authorizenet_customer_profile_id,
                "paymentProfile": {
                    "billTo": customer_address,
                    "payment": {
                        "creditCard": {
                            "cardNumber": card_number,
                            "expirationDate": card_expiry,
                        }
                    },
                },
            }
        }

        response = requests.post(
            settings.AUTHORIZE_NET_TRANSACTION_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

        response_data = json.loads(response.content.decode("utf-8-sig"))

        return response_data

    def create_customer_profile(self, card_number, card_expiry, user, customer_address):
        merchant_auth = self._get_merchant_auth()

        payload = {
            "createCustomerProfileRequest": {
                "merchantAuthentication": merchant_auth,
                "profile": {
                    "merchantCustomerId": user.username,
                    "description": user.email,
                    "email": user.email,
                    "paymentProfiles": {
                        "customerType": "individual",
                        "billTo": customer_address,
                        "payment": {
                            "creditCard": {
                                "cardNumber": card_number,
                                "expirationDate": card_expiry,
                            }
                        },
                    },
                },
                "validationMode": "testMode",
            }
        }

        response = requests.post(
            settings.AUTHORIZE_NET_TRANSACTION_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

        response_data = json.loads(response.content.decode("utf-8-sig"))

        if authorizenet_customer_profile_id := response_data.get("customerProfileId"):
            user.user_information.authorizenet_customer_profile_id = (
                authorizenet_customer_profile_id
            )
            user.user_information.save(
                update_fields=["authorizenet_customer_profile_id"]
            )

        return response_data

    def create_customer_profile_from_transaction(self):
        merchant_auth = self._get_merchant_auth()

        payload = {
            "createCustomerProfileFromTransactionRequest": {
                "merchantAuthentication": merchant_auth,
                "transId": "2239321185",
            }
        }

        response = requests.post(
            settings.AUTHORIZE_NET_TRANSACTION_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

        response_data = json.loads(response.content.decode("utf-8-sig"))

        return response_data

    def get_customer_profile(self, customer_profile_id):
        merchant_auth = self._get_merchant_auth()

        payload = {
            "getCustomerProfileRequest": {
                "merchantAuthentication": merchant_auth,
                "customerProfileId": customer_profile_id,
                "includeIssuerInfo": "true",
            }
        }

        response = requests.post(
            settings.AUTHORIZE_NET_TRANSACTION_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

        response_data = json.loads(response.content.decode("utf-8-sig"))

        return response_data

    def get_customer_payment_profile(
        self, customer_profile_id, customer_payment_profile_id
    ):
        merchant_auth = self._get_merchant_auth()

        payload = {
            "getCustomerPaymentProfileRequest": {
                "merchantAuthentication": merchant_auth,
                "customerProfileId": customer_profile_id,
                "customerPaymentProfileId": customer_payment_profile_id,
            }
        }

        response = requests.post(
            settings.AUTHORIZE_NET_TRANSACTION_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

        response_data = json.loads(response.content.decode("utf-8-sig"))

        return response_data


class TossPayments:
    def __init__(self, secret_key):
        self.secret_key = string_to_base64(f"{secret_key}:")

    def _get_payment_headers(self):
        payment_headers = {
            "Authorization": f"Basic {self.secret_key}",
            "Content-Type": "application/json",
        }
        return payment_headers

    def authorize_payment(self, amount, order_id, payment_key):
        payment_headers = self._get_payment_headers()

        payload = {
            "paymentKey": payment_key,
            "amount": amount,
            "orderId": order_id,
        }

        response = requests.post(
            f"{settings.TOSS_API_URL}payments/confirm",
            data=json.dumps(payload),
            headers=payment_headers,
        )

        return response.status_code, response.json()

    def cancel_payment(self, payment_key: str, reason: str = "", amount: int = None):
        payment_headers = self._get_payment_headers()

        payload = {"cancelReason": reason}

        if amount:
            payload["cancelAmount"] = amount

        response = requests.post(
            f"{settings.TOSS_API_URL}payments/{payment_key}/cancel",
            data=json.dumps(payload),
            headers=payment_headers,
        )

        return response.status_code, response.json()
