from werkzeug.security import generate_password_hash

from apis.auth.model.auth import User
from apis.core.db import db


class UserService:
    @staticmethod
    def findByUsername(username):
        """username 으로 user 조회"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def findAll():
        """모든 user 조회"""
        return User.query.all()

    @staticmethod
    def createUser(user_info):
        """create user"""
        username = user_info.get('username')
        password = user_info.get('password')
        email = user_info.get('email')
        role = user_info.get('role')
        existed_user = User.query.filter_by(username=username).first()
        if existed_user:
            return False
        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def findById(cls, user_id):
        """find by user_id"""
        by_user_id = User.query.filter_by(id=user_id).first()
        return by_user_id

    @classmethod
    def updateUser(cls, user, user_info):
        """update user"""
        user.username = user_info.get('username')
        user.password = generate_password_hash(user_info.get('password'))
        user.email = user_info.get('email')
        user.role = user_info.get('role')
        db.session.commit()
        return user

    @staticmethod
    def deleteUser(user):
        """delete user"""
        db.session.delete(user)
        db.session.commit()
