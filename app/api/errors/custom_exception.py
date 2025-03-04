class CustomAppException(Exception):
    """Base exception for the application"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
