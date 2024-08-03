from random import SystemRandom
from urllib.parse import urlencode
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from attrs import define
from oauthlib.common import UNICODE_ASCII_CHARACTER_SET

from django_project import settings


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


class GoogleLoginFlowService:

    # create a URL for the OAuth2 callback endpoint
    API_URI = reverse_lazy('api:google-oauth2:login:callback')

    # URL used to initiate the OAuth2 authorization process with Google
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    # URL to exchange the authorization code for an access token
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    # URL to fetch user profile information from Google after authentication
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    # scopes define the level of access the app is requesting - in this case access to user email, profile information, and basic OpenID Connect information
    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]

    def __init__(self):
        self._credentials = google_login_get_credentials()

    @staticmethod
    # Generates a random state token used to prevent CSRF attacks
    def _generate_state_session_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        rand = SystemRandom()
        state = "".join(rand.choice(chars) for _ in range(length))
        return state

    # Constructs the full redirect URI to which Google will redirect after user authentication
    def _get_redirect_uri(self):
        domain = settings.BASE_BACKEND_URL
        api_uri = self.API_URI
        redirect_uri = f'{domain}{api_uri}'
        return redirect_uri

    # constructs the Google authorization URL
    def get_authorization_url(self):
        redirect_uri = self._get_redirect_uri()

        state = self._generate_state_session_token()

        params = {
            "response_type": "code",
            "client_id": self._credentials.client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(self.SCOPES),
            "state": state,
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "select_account",
        }

        query_params = urlencode(params)
        authorization_url = f"{self.GOOGLE_AUTH_URL}?{query_params}"

        return authorization_url, state
