from rest_framework.decorators import api_view
from django.shortcuts import redirect

from authentication.services import GoogleLoginFlowService


@api_view
class GoogleLoginRedirectAPI:
    def get(self, request, *args, **kwargs):
        google_login_flow = GoogleLoginFlowService()

        authorization_url, state = google_login_flow.get_authorization_url

        # state is added to prevent cross-site request forgery attacks (CSRF)
        request.session['google_oauth2_state'] = state

        # redirect to the obtained Google authorization url
        return redirect(authorization_url)
