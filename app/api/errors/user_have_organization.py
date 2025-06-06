from app.api.errors.custom_exception import CustomAppException


class UserHaveOrgException(CustomAppException):
    def __init__(self, message: str = "User already have an organization") -> None:
        super().__init__(message)
