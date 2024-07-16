def success_response(message, data, status_code=200):
    """
    All went well, and (usually) some data was returned.
        - required: status, data
        - optional: n/a
    """
    return {
        'status': 'success',
        'message': message,
        'data': data
    }, status_code


def fail_response(message, data, status_code=400):
    """
    There was a problem with the data submitted, or some pre-condition of the API call wasn't satisfied.
        - required: status, data
        - optional: n/a
    """
    return {
        'status': 'fail',
        'message': message,
        'data': data
    }, status_code


def error_response(message, status_code=500):
    """
    An error occurred in processing the request, i.e. an exception was thrown.
        - required: status, message
        - optional: code, data
    """
    return {
        'status': 'error',
        'message': message
    }, status_code
