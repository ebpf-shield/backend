from app.api.errors.custom_exception import CustomAppException


class InvalidPasswordException(CustomAppException):
    def __init__(self, message="Invalid password"):
        super().__init__(message)
