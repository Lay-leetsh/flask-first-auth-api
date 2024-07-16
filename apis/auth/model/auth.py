from werkzeug.security import generate_password_hash, check_password_hash

from apis.core.db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(255), unique=True, nullable=False)

    def set_password(self, password):
        """Set the password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check the password is correct or not"""
        return check_password_hash(self.password, password)

    def to_dict(self):
        """Convert the user object to a dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }
