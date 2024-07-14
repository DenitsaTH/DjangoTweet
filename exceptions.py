from django.core.exceptions import PermissionDenied


class PostNotFoundException(Exception):
    def __init__(self, message="Post not found"):
        self.message = message


class UnauthorizedAccessException(PermissionDenied):
    def __init__(self, message="Owner required"):
        self.message = message
