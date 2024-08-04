from django.core.exceptions import PermissionDenied


class PostNotFoundException(Exception):
    def __init__(self, message="Post not found"):
        self.message = message


class UnauthorizedAccessException(PermissionDenied):
    def __init__(self, message="Owner required"):
        self.message = message


class ApplicationError(Exception):
    def __init__(self, message):
        super().__init__(message)

        self.message = message
