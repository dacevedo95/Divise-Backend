import base64
from datetime import datetime, timedelta
import os
import datetime

from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    country_calling_code = db.Column(db.String(8))
    phone_number = db.Column(db.String(32), index=True, unique=True)
    full_phone_number = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    verified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    transactions = db.relationship('Transaction', backref='author', lazy='dynamic')
    recurring_transactions = db.relationship('RecurringTransaction', backref='recurring_author', lazy='dynamic')
    settings = db.relationship('Settings', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User: {0}>'.format(self.phone_number)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        data = {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'countryCallingCode': self.country_calling_code,
            'phoneNumber': self.phone_number,
            'createdAt': self.created_at
        }
        return data

    def from_dict(self, data, new_user=False):
        self.first_name = data['firstName']
        self.last_name = data['lastName']
        self.country_calling_code = data['countryCode']
        self.phone_number = data['phoneNumber']
        self.full_phone_number = '+' + data['countryCode'] + data['phoneNumber']

        if new_user and 'password' in data:
            self.set_password(password=data['password'])

    def reset_password(self, newPassword):
        self.set_password(password=newPassword)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(128))
    category = db.Column(db.String(32))
    price = db.Column(db.Float())
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'createdAt': self.created_at,
            'canEdit': True
        }
        return data

    def from_dict(self, data, author=None):
        self.name = data['name']
        self.category = data['category']
        self.price = data['price']
        self.created_at = datetime.datetime.strptime(data['createdAt'], '%Y-%m-%d')

        if author:
            self.author = author

class RecurringTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(128))
    category = db.Column(db.String(32))
    price = db.Column(db.Float())
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    effective_at = db.Column(db.DateTime, default=datetime.datetime(year=datetime.datetime.utcnow().year, month=datetime.datetime.utcnow().month, day=1))

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'createdAt': self.created_at,
            'effectiveDate': self.effective_at,
            'canEdit': False
        }
        return data

    def from_dict(self, data, author=None):
        self.name = data['name']
        self.category = data['category']
        self.price = data['price']
        self.created_at = datetime.datetime.strptime(data['createdAt'], '%Y-%m-%d')
        self.effective_at = datetime.datetime.strptime(data['effectiveAt'], '%Y-%m')

        if author:
            self.recurring_author = author

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    needs_percentage = db.Column(db.Float())
    wants_percentage = db.Column(db.Float())
    savings_percentage = db.Column(db.Float())
    income = db.Column(db.Float())
    effective_at = db.Column(db.DateTime, default=datetime.datetime(year=datetime.datetime.utcnow().year, month=datetime.datetime.utcnow().month, day=1))

    def to_dict(self):
        data = {
            'needsPercentage': self.needs_percentage,
            'wantsPercentage': self.wants_percentage,
            'savingsPercentage': self.savings_percentage,
            'income': self.income
        }
        return data

    def from_dict(self, data, user=None):
        self.needs_percentage = data['needsPercentage']
        self.wants_percentage = data['wantsPercentage']
        self.savings_percentage = data['savingsPercentage']
        self.income = data['income']
        self.effective_at = datetime.datetime.strptime(data['effectiveAt'], '%Y-%m')

        if user:
            self.user = user
