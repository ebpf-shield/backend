from app.api.errors.custom_exception import CustomAppException


class NoUserWithEmailException(CustomAppException):
    def __init__(self, message="Couldn't find your account"):
        super().__init__(message)
