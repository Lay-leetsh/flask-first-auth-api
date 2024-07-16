from flask import request, session
from flask_jwt_extended import create_access_token
from flask_restx import Namespace, fields, Resource

from apis.auth.service.auth_service import AuthService
from apis.core.custom_exception import SignInError, UserNotFoundError, SignUpFail
from apis.core.response import success_response
from apis.users.service.user_service import UserService

auth_ns = Namespace('auth', description='About authentication operations')

auth_login_model = auth_ns.model('AuthLogin', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password')
})

auth_register_model = auth_ns.model('AuthRegister', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password'),
    'email': fields.String(required=True, description='The email address'),
    'role': fields.String(required=None, description='The role'),
})

response_model = auth_ns.model('Response', {
    'status': fields.String(description='Response status'),
    'message': fields.String(description='Response message', required=False),
    'data': fields.String(description='Response data'),
})


@auth_ns.route('/login')
class AuthLogin(Resource):
    @auth_ns.expect(auth_login_model, validate=True)
    @auth_ns.response(200, 'Success', response_model)
    @auth_ns.response(401, 'Unauthorized', response_model)
    @auth_ns.response(500, 'Internal Server Error', response_model)
    def post(self):
        """user login"""
        # try:
        login_info = request.get_json()
        username = login_info['username']
        password = login_info['password']
        user = UserService.findByUsername(username)
        if not user:
            raise UserNotFoundError("존재하지 않는 사용자입니다.")

        if not AuthService.authenticate(user, password):
            raise SignInError("아이디/비밀번호가 일치하지 않습니다.")

        # access_token 생성 및 session 저장
        access_token = create_access_token(identity=username)
        session['jwt'] = access_token
        return success_response("Logged in successfully",
                                {"access_token": access_token},
                                200)


@auth_ns.route('/register')
class AuthRegister(Resource):
    @auth_ns.expect(auth_register_model, validate=True)
    @auth_ns.marshal_with(response_model)
    def post(self):
        """user registration"""
        register_info = request.get_json()
        username = register_info['username']
        by_username = UserService.findByUsername(username)
        if by_username:
            raise SignUpFail("이미 등록된 사용자입니다.")
        else:
            new_user = AuthService.register(register_info)
            if new_user:
                user_data = new_user.to_dict()
                return success_response("User registered successfully",
                                        user_data,
                                        201)
            else:
                raise SignUpFail("사용자 등록을 실패하였습니다.")
