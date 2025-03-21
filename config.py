import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    SQLALCHEMY_DATABASE_URI = "postgresql://mikemUser:manoti2929@localhost/edu-db"  # Change to PostgreSQL/MySQL in production
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")

    # MPesa API Credentials from Safaricom Daraja
    MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY", "3A58YZAyOWt01M6jeiwa7wAcxDbJkS70hEDG6RzRoiAkqY2u")
    MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET", "9tfpxQjARy9knEbf3L9TQCSvwZlt9yYzIqGGwgHatAG5biNhbD8IvjCrmlCHlOwd")
    MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE", "N/A")  # Update when you get a valid shortcode
    MPESA_PASSKEY = os.getenv("MPESA_PASSKEY", "your_passkey")  # Required for STK Push transactions
    MPESA_BASE_URL = "https://sandbox.safaricom.co.ke"  # Change to production URL when live
    BASE_URL = "https://your-backend-url.com"  # Change to your actual backend URL
    MPESA_INITIATOR_NAME = os.getenv("MPESA_INITIATOR_NAME", "your_initiator")  # Required for B2C, C2B, etc.
    MPESA_SECURITY_CREDENTIAL = os.getenv("MPESA_SECURITY_CREDENTIAL", "your_security_credential")  # Required for B2C, C2B, etc.
