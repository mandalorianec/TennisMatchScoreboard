from src.exceptions.base_exception import OwnBaseException


class ValidationException(OwnBaseException):
    def __init__(self, error_message: str):
        self.error_message = error_message
        self.error_code = "400 Bad request"


class ControllerNotFoundException(OwnBaseException):
    def __init__(self, error_message: str):
        self.error_message: str = error_message
        self.error_code: str = "404 Not Found"


class UnsupportedMethodException(OwnBaseException):
    def __init__(self, error_message: str):
        self.error_message = error_message
        self.error_code: str = "405 Method Not Allowed"
