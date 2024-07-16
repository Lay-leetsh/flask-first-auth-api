class CustomUserError(Exception):
    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_message = error_message


class UserNotFoundError(CustomUserError):
    def __init__(self, error_message):
        status_code = 404
        super().__init__(status_code, error_message)


class SignUpFail(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        super().__init__(status_code, error_message)


class SignInError(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        super().__init__(status_code, error_message)
