from django.core.exceptions import ImproperlyConfigured
from django_project import settings
from attrs import define


@define
class GoogleLoginCredentials:
    client_id: str
    client_secret: str
    project_id: str


def google_login_get_credentials() -> GoogleLoginCredentials:
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET
    project_id = settings.GOOGLE_OAUTH2_PROJECT_ID

    if not client_id:
        raise ImproperlyConfigured('GOOGLE_OAUTH2_CLIENT_ID missing in env.')

    if not client_secret:
        raise ImproperlyConfigured(
            'GOOGLE_OAUTH2_CLIENT_SECRET missing in env.')

    if not project_id:
        raise ImproperlyConfigured('GOOGLE_OAUTH2_PROJECT_ID missing in env.')

    credentials = GoogleLoginCredentials(
        client_id=client_id,
        client_secret=client_secret,
        project_id=project_id
    )

    return credentials
