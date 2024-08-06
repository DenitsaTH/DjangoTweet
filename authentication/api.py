from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
import logging

from authentication.services import GoogleLoginFlowService
from users.models import User


logger = logging.getLogger(__name__)


@swagger_auto_schema(method='get', tags=['public'], operation_summary="Redirects to Google OAuth2 login")
@api_view(['GET'])
def google_login_redirect_api(request, *args, **kwargs):

    google_login_flow = GoogleLoginFlowService()

    authorization_url, state = google_login_flow.get_authorization_url()

    # state is added to prevent cross-site request forgery attacks (CSRF)
    request.session['google_oauth2_state'] = state
    request.session.save()

    # redirect to the obtained Google authorization url
    return redirect(authorization_url)


class GoogleLoginInputSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    state = serializers.CharField(required=False)


@api_view(['GET'])
def google_login_api(request, *args, **kwargs):
    input_serializer = GoogleLoginInputSerializer(data=request.GET)
    input_serializer.is_valid(raise_exception=True)

    validated_data = input_serializer.validated_data

    code = validated_data.get("code")
    error = validated_data.get("error")
    state = validated_data.get("state")

    if error is not None:
        return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

    if code is None or state is None:
        return Response({'error': 'Code and state required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify the state parameter against the value stored in the session to prevent CSRF attacks
    session_state = request.session['google_oauth2_state']

    if session_state is None:
        return Response({'error': 'CSRF check failed.'}, status=status.HTTP_400_BAD_REQUEST)

    del request.session['google_oauth2_state']

    if state != session_state:
        return Response({'error': 'CSRF check failed'}, status=status.HTTP_400_BAD_REQUEST)

    # Use GoogleLoginFlowService to exchange the authorization code for tokens and fetch user information
    google_login_flow = GoogleLoginFlowService()

    google_tokens = google_login_flow.get_tokens(code=code)
    id_token_decoded = google_tokens.decode_id_token()
    # user_info = google_login_flow.get_user_info(google_tokens=google_tokens)

    # Retrieve the user
    user_email = id_token_decoded['email']
    user = get_object_or_404(User, email=user_email)

    if user.is_sandboxed or user.is_deleted:
        return Response({'error': f'User with email {user_email} is not found or inactive.'}, status=status.HTTP_404_NOT_FOUND)

    # Log the user in
    login(request, user)

    # Create or retrieve the token for the client to further interact with login endpoints
    user_token, _ = Token.objects.get_or_create(user=user)

    result = {
        'token': user_token.key,
        'id_token_decoded': id_token_decoded,
        # 'user_info': user_info
    }

    return Response(result)
