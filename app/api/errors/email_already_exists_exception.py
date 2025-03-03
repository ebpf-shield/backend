from app.api.errors.custom_exception import CustomAppException


class EmailAlreadyExistsException(CustomAppException):
    def __init__(self, message="This email is already registered."):
        super().__init__(message)
