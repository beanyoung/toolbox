class ToolBoxBaseException(Exception):
    status_code = 500
    error_name = 'base_exception'

    def __init__(self, message):
        self.message = message

    def to_dict(self):
        return dict(error_name=self.error_name, message=self.message)


class UnknownError(ToolBoxBaseException):
    status_code = 500
    error_name = 'unknown_error'

    def __init__(self, e):
        self.message = '{}'.format(e)


class BadRequest(ToolBoxBaseException):
    status_code = 400
    error_name = 'bad_request'

    def __init__(self, message=None):
        self.message = message
