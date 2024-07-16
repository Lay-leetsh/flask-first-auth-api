from apis.auth.model.auth import User
from apis.core.db import db


class AuthService:
    @staticmethod
    def authenticate(user, password):
        """아이디/패스워드 검증"""
        return user.check_password(password)

    @staticmethod
    def register(register_info):
        """신규 사용자 저장"""
        username = register_info.get('username')
        password = register_info.get('password')
        email = register_info.get('email')
        role = register_info.get('role')
        existed_user = User.query.filter_by(username=username).first()
        if existed_user:
            return False
        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
