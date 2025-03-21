from flask import Blueprint, jsonify
from flask import Blueprint, request, jsonify
from app.mpesa import MpesaAPI
from app.mpesa import get_mpesa_access_token

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return jsonify({"message": "Welcome to the Apartment Management System!"})



@main_bp.route("/get-access-token", methods=["GET"])
def fetch_token():
    token = get_mpesa_access_token()
    if token:
        return jsonify({"access_token": token})
    return jsonify({"error": "Failed to fetch token"}), 400





mpesa_bp = Blueprint("mpesa", __name__)

@mpesa_bp.route("/mpesa/house_payment", methods=["POST"])
def house_payment():
    data = request.json
    phone_number = data.get("phone_number")
    amount = data.get("amount")
    account_reference = data.get("account_reference")
    response = MpesaAPI.process_house_payment(phone_number, amount, account_reference)
    return jsonify(response)

@mpesa_bp.route("/mpesa/water_payment", methods=["POST"])
def water_payment():
    data = request.json
    phone_number = data.get("phone_number")
    amount = data.get("amount")
    response = MpesaAPI.process_water_bill_payment(phone_number, amount)
    return jsonify(response)

@mpesa_bp.route("/mpesa/callback", methods=["POST"])
def mpesa_callback():
    data = request.json
    response = MpesaAPI.confirm_payment(data)
    return jsonify(response)

@mpesa_bp.route("/mpesa/validate", methods=["POST"])
def mpesa_validate():
    data = request.json
    response = MpesaAPI.validate_payment(data)
    return jsonify(response)
