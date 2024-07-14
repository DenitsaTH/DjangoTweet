from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from django_project.serializers import UserProfileSerializer, UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser

from users.models import User
from users.services import create_user, get_total_likes_and_posts, upload_profile_picture


@swagger_auto_schema(method='get', auto_schema=None)
@api_view(['GET'])
def home_page(request):
    return HttpResponse("Welcome:)")


@swagger_auto_schema(method='post', tags=['public'], request_body=UserSerializer)
@api_view(['POST'])
def register(request):
    """
    post:
    Register a new user with an email and password

    **Parameters**:
    - request (`HttpRequest`): The HTTP request containing user registration data.

    **Request Body**:
    - email (`str`): The email address of the user.
    - password (`str`): The password for the user account.

    **Responses**:
    - 201 Created: Registration successful. Login to continue.
    - 400 Bad Request: Invalid data provided. The response will include error details.

    **Example response on success:**

    "Registration successful! Login to continue"

    **Example response on failure:**

    {
        "email": ["Enter a valid email address."]
    }
    """

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        if create_user(serializer, email, password):
            return Response('Registration successful! Login to continue',
                            status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', tags=['public'], request_body=UserSerializer)
@api_view(['POST'])
def login(request):
    """
    post:
    Authenticate a user with provided email and password

    This endpoint verifies the provided email and password combination against
    the stored user credentials. If authentication succeeds, it generates a new
    access token for the user session. The token can be used for subsequent
    authenticated requests through the **Authorize** button. Input 'Token *token_value*'
    in the Value field.

    **Parameters:**
    - request (`HttpRequest`): The HTTP request containing user login credentials.

    **Request Body:**
    - email (`str`): The email address of the user.
    - password (`str`): The password for the user account.

    **Responses:**
    - 200 OK: Authentication successful. Returns a token and user details.
    - 401 Unauthorized: User profile is inactive or does not exist.
    - 404 Not Found: Invalid email or password provided.

    **Example response on success:**

    {
    "token": generated token,
    "user": {
        "id": 1,
        "email": "user@example.com"
    }

    **Example response when profile is inactive:**

    {
        "detail": "Profile inactive"
    }

    **Example response on invalid credentials:**

    {
        "detail": "Not found."
    }
    """

    user = get_object_or_404(User, email=request.data['email'])

    if not user.check_password(request.data['password']):
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if user.is_deleted or user.is_sandboxed:
        return Response({'detail': 'Profile inactive'}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({'token': token.key, 'user': serializer.data})


@swagger_auto_schema(method='post', tags=['public'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    post:
    Logout the authenticated user and delete the current session token

    This endpoint logs out the currently authenticated user by deleting the
    authentication token associated with the user session. After successful
    logout, the user will need to re-authenticate to access protected resources.

    **Parameters:**
    - request (`HttpRequest`): The HTTP request containing the user's authentication token.

    **Responses:**
    - 200 OK: Logout successful. The user's session token has been invalidated.

    **Example response on success:**

    {
        "detail": "Logout successful."
    }
    """

    try:
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    except Exception:
        return Response({'detail': 'Failed to log out.'},
                        status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', tags=['users'], request_body=UserProfileSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    put:
    Update profile information of the currently authenticated user

    This endpoint allows the authenticated user to update their names and/or 
    description. The request can include partial data to update only specific 
    fields. Upon successful update, the updated user profile object is returned.

    **Parameters**:
    - request (`HttpRequest`): The HTTP request containing the user's authentication token
                            and the updated profile data.

    **Request Body:**
    Provide fields you want to update. All fields are optional.

    **Responses:**
    - 201 Created: Profile information successfully updated. Returns the updated user profile object.
    - 400 Bad Request: If the request data is invalid or profile update fails.

    **Example response on success:**

    {
        "id": 1,
        "first_name": "new_first_name",
        "last_name": "new_last_name",
        "description": "Updated description"
    }
    """

    user_profile = request.user

    serializer = UserProfileSerializer(
        instance=user_profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='put',
    tags=['users'],
    manual_parameters=[
        openapi.Parameter(
            'profile_picture',
            openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True
        ),
    ]
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_profile_picture(request):
    """
    put:
    Update the profile picture of the currently authenticated user

    This endpoint allows the authenticated user to update their profile picture.
    The request must include a valid image file as profile_picture. Upon
    successful update, the updated user object is returned with the updated profile
    picture URL.

    **Parameters**:
    - request (`HttpRequest`): The HTTP request containing the user's authentication token
                            and the updated profile picture.

    **Request Body:**
    - profile_picture (`binary`): The new profile picture image file.

    **Responses:**
    - 201 Created: Profile picture successfully updated. Returns the updated user object.
    - 400 Bad Request: If the request data is invalid or profile picture update fails.

    **Example response:**

      {
          "id": 1,
          "email": "user@example.com",
          "profile_picture": "http://example.com/media/profiles/user123/profile.jpg",
      }

    **Example response on error:**

    {
        "profile_picture": ["Upload a valid image file."]
    }
    """

    user = request.user

    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        upload_profile_picture(request.data.get('profile_picture'), user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_OK)


@swagger_auto_schema(method='get', tags=['users'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_likes_and_posts(request):
    """
    get:
    Retrieve total likes and posts created by the currently authenticated user

    Returns the total number of likes and posts created by the
    currently authenticated user. The likes represent the total number of likes
    the user's posts have accumulated, while posts created indicate the total
    number of posts created by the user.

    **Parameters**:
    - request (`HttpRequest`): The HTTP request containing the user's authentication token.

    **Responses**:
    - 200 OK: Returns total likes and posts created by the user.
    - 401 Unauthorized: If the request is not authenticated or the token is invalid.

    **Example response on success:**

    {
        "Total likes": 123,
        "Total posts created": 45
    }
    """

    likes, posts = get_total_likes_and_posts(request.user)

    return Response({"Total likes": likes,
                     "Total posts created": posts})
