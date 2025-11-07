from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserRecord(db.Model):
    __tablename__ = "userRecords"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    mobileNumber = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable=False)
