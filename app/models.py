from app import db
from flask_login import UserMixin
from datetime import datetime
import hashlib
import os

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scans = db.relationship('Scan', backref='user', lazy=True)

    def set_password(self, password):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        self.password_hash = salt.hex() + key.hex()

    def check_password(self, password):
        if not self.password_hash:
            return False
        salt = bytes.fromhex(self.password_hash[:64])
        key = bytes.fromhex(self.password_hash[64:])
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return key == new_key

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    barcode = db.Column(db.String(50), nullable=False)
    recyclable = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)