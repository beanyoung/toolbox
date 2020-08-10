from functools import wraps

from flask import (
    make_response,
    request,
)

from toolbox.exceptions import (
    BadRequest,
    ToolBoxBaseException,
    UnknownError,
)


def make_response_from_error(e):
    if isinstance(e, ToolBoxBaseException):
        return make_response(e.to_dict(), e.status_code)
    unknown_error = UnknownError(e)
    return make_response_from_error(unknown_error)


def rest(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return make_response_from_error(
                BadRequest('unsupported content type'))
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return make_response_from_error(e)
    return decorated_function
