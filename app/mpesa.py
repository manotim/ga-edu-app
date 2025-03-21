import requests
import json
import base64
from datetime import datetime
from flask import current_app
from requests.auth import HTTPBasicAuth

def get_mpesa_access_token():
    """Fetch access token from Safaricom MPesa API"""
    ACCESS_TOKEN_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    # Read credentials from Flask config
    consumer_key = current_app.config["MPESA_CONSUMER_KEY"]
    consumer_secret = current_app.config["MPESA_CONSUMER_SECRET"]
    
    # Make request
    response = requests.get(ACCESS_TOKEN_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None

class MpesaAPI:
    @staticmethod
    def get_access_token():
        """Fetch the MPesa access token."""
        url = f"{current_app.config['MPESA_BASE_URL']}/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(url, auth=(
            current_app.config['MPESA_CONSUMER_KEY'],
            current_app.config['MPESA_CONSUMER_SECRET']
        ))
        if response.status_code == 200:
            return response.json().get("access_token")
        return None

    @staticmethod
    def process_house_payment(phone_number, amount, account_reference):
        """Initiate house payment using Paybill (STK Push)."""
        access_token = MpesaAPI.get_access_token()
        if not access_token:
            return {"error": "Failed to get access token"}

        url = f"{current_app.config['MPESA_BASE_URL']}/mpesa/stkpush/v1/processrequest"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(
            f"{current_app.config['MPESA_SHORTCODE']}{current_app.config['MPESA_PASSKEY']}{timestamp}".encode()
        ).decode()

        payload = {
            "BusinessShortCode": current_app.config['MPESA_SHORTCODE'],
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": current_app.config['MPESA_SHORTCODE'],
            "PhoneNumber": phone_number,
            "CallBackURL": f"{current_app.config['BASE_URL']}/mpesa/callback/",
            "AccountReference": account_reference,
            "TransactionDesc": "House Rent Payment"
        }

        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    @staticmethod
    def process_water_bill_payment(phone_number, amount):
        """Send money for water bill payment (B2C API)."""
        access_token = MpesaAPI.get_access_token()
        if not access_token:
            return {"error": "Failed to get access token"}

        url = f"{current_app.config['MPESA_BASE_URL']}/mpesa/b2c/v1/paymentrequest"
        payload = {
            "InitiatorName": current_app.config['MPESA_INITIATOR_NAME'],
            "SecurityCredential": current_app.config['MPESA_SECURITY_CREDENTIAL'],
            "CommandID": "BusinessPayment",
            "Amount": amount,
            "PartyA": current_app.config['MPESA_SHORTCODE'],
            "PartyB": phone_number,
            "Remarks": "Water Bill Payment",
            "QueueTimeOutURL": f"{current_app.config['BASE_URL']}/mpesa/timeout/",
            "ResultURL": f"{current_app.config['BASE_URL']}/mpesa/result/",
            "Occasion": "Water Bill"
        }

        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    @staticmethod
    def validate_payment(data):
        """Handle payment validation callback."""
        current_app.logger.info("Validation Data Received: %s", data)
        return {"ResultCode": 0, "ResultDesc": "Accepted"}

    @staticmethod
    def confirm_payment(data):
        """Handle payment confirmation callback."""
        current_app.logger.info("Confirmation Data Received: %s", data)
        return {"ResultCode": 0, "ResultDesc": "Success"}
