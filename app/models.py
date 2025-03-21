from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('tenant', 'landlord', 'admin', name='user_role'), nullable=False) # Added name='user_role'
    tenants = db.relationship('Tenant', backref='user')
    landlords = db.relationship('Landlord', backref='user')

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'))
    agreement_pdf = db.Column(db.String(255))
    payments = db.relationship('Payment', backref='tenant', lazy=True)
    water_bills = db.relationship('WaterBill', backref='tenant', lazy=True)

class Landlord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    apartments = db.relationship('Apartment', backref='landlord', lazy=True)

class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'), nullable=False)
    houses = db.relationship('House', backref='apartment', lazy=True)

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)
    number = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.Enum('available', 'booked', name='house_status'), default='available', nullable=False) # Added name='house_status'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.Enum('pending', 'successful', 'failed', name='payment_status'), default='pending', nullable=False) # Added name='payment_status'
    date_paid = db.Column(db.DateTime, default=datetime.utcnow)

class WaterBill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    units_consumed = db.Column(db.Float, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('pending', 'paid', name='water_bill_status'), default='pending', nullable=False) # Added name='water_bill_status'
    date_issued = db.Column(db.DateTime, default=datetime.utcnow)