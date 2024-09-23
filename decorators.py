from functools import wraps
from django.utils import timezone

from users.models import UserActivity


def log_activity(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        request = args[0]
        user = request.user
        username = user.username if user.is_authenticated else 'Anonymous'
        action = func.__name__
        current_time = timezone.now()

        action_log = UserActivity(
            username=username, action=action, timestamp=current_time
        )
        action_log.save()

        return func(*args, **kwargs)

    return func_wrapper
