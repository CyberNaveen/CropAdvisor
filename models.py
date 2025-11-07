from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class UserRecord(db.Model):
    __tablename__ = "userRecords"
    username = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    mobileNumber = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable=False)
