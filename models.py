from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UserRecord(db.Model):
    __tablename__ = "userRecords"

    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(50), primary_key=True, nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    mobileNumber = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(255), nullable=False)  # hashed password
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
