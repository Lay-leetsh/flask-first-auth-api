import traceback

from sqlalchemy.exc import InvalidRequestError

from apis.core.custom_exception import CustomUserError
from apis.core.response import error_response


def error_handle(api):
    """에러 핸들러 : error_response()로 error_message와 status_code를 전달하여 반환"""

    @api.errorhandler(AttributeError)
    def handle_attribute_error(e):
        traceback.print_exc()
        return error_response("서버 상에서 오류가 발생했습니다.", 500)

    @api.errorhandler(KeyError)
    def handle_key_error(e):
        traceback.print_exc()
        return error_response("데이터베이스에서 값을 가져오는데 문제가 발생하였습니다.", 500)

    @api.errorhandler(TypeError)
    def handle_type_error(e):
        traceback.print_exc()
        return error_response("데이터의 값이 잘못 입력되었습니다", 500)

    @api.errorhandler(ValueError)
    def handle_value_error(e):
        traceback.print_exc()
        return error_response("데이터에 잘못된 값이 입력되었습니다.", 500)

    @api.errorhandler(InvalidRequestError)
    def handle_data_error(e):
        """validate_params 정규식 에러
        validate_params rules에 위배될 경우 발생되는 에러 메시지를 처리하는 함수
        """
        traceback.print_exc()
        return error_response("형식에 맞는 값을 입력해주세요", 400)

    @api.errorhandler(CustomUserError)
    def handle_custom_error(e):
        traceback.print_exc()
        return error_response(e.error_message, e.status_code)

    @api.errorhandler(Exception)
    def handle_base_error(e):
        traceback.print_exc()
        return error_response("서버 상에서 오류가 발생했습니다.", 500)
