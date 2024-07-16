from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, fields, Resource

from apis.core.custom_exception import SignUpFail, UserNotFoundError
from apis.core.response import success_response
from apis.users.service.user_service import UserService

user_ns = Namespace('users', description='About user operations')

user_request_model = user_ns.model('Users', {
    'user_id': fields.Integer(required=True, description='The unique identifier')
})

user_modification_model = user_ns.model('UserModification', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password'),
    'email': fields.String(required=True, description='The email address'),
    'role': fields.String(required=None, description='The role'),
})

response_model = user_ns.model('Response', {
    'status': fields.String(description='Response status'),
    'message': fields.String(description='Response message', required=False),
    'data': fields.String(description='Response data'),
})


@user_ns.route('')
class UserManager(Resource):
    @jwt_required()
    def get(self):
        """find all users"""
        current_user = get_jwt_identity()
        print('Current user: %s' % current_user)
        all_users = UserService.findAll()
        users_dict = [user.to_dict() for user in all_users]
        return success_response(None, users_dict)

    @jwt_required()
    def post(self):
        """create a new user"""
        current_user = get_jwt_identity()
        print('Current user: %s' % current_user)
        user_info = request.get_json()
        new_user = UserService.createUser(user_info)
        if not new_user:
            return SignUpFail("사용자 등록을 실패하였습니다.")
        return success_response(None, new_user.to_dict())


@user_ns.route('/<int:user_id>')
class UserManager2(Resource):
    @jwt_required()
    @user_ns.marshal_with(response_model)
    def get(self, user_id):
        """find a user by id"""
        current_user = get_jwt_identity()
        print('Current user: %s' % current_user)
        user = UserService.findById(user_id)
        if not user:
            return UserNotFoundError("존재하지 않는 사용자입니다.")
        return success_response(None, user.to_dict())

    @jwt_required()
    @user_ns.expect(user_modification_model, validate=True)
    @user_ns.marshal_with(response_model)
    def put(self, user_id):
        """update a user"""
        current_user = get_jwt_identity()
        print('Current user: %s' % current_user)
        user = UserService.findById(user_id)
        if not user:
            return UserNotFoundError("존재하지 않는 사용자입니다.")
        modified_user_info = request.get_json()
        modified_user = UserService.updateUser(user, modified_user_info)
        if not modified_user:
            return SignUpFail("사용자 정보 수정을 실패하였습니다.")
        return success_response(None, modified_user.to_dict())

    @jwt_required()
    @user_ns.marshal_with(response_model)
    def delete(self, user_id):
        """delete a user"""
        current_user = get_jwt_identity()
        print('Current user: %s' % current_user)
        user = UserService.findById(user_id)
        if not user:
            return UserNotFoundError("존재하지 않는 사용자입니다.")
        UserService.deleteUser(user)
        return success_response({"message": "User deleted"}, None)
