from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django_project.serializers import PostSerializer, SubmitPostSerializer
from posts.services import get_all_posts, remove_post, switch_like_status
from exceptions import PostNotFoundException, UnauthorizedAccessException
from decorators import log_activity


@swagger_auto_schema(
    method='get',
    tags=['posts'],
    manual_parameters=[
        openapi.Parameter('pages', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter(
            'items_per_page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER
        ),
    ],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request):
    """
    get:
    Retrieve paginated list of posts

    This endpoint allows an authenticated user to retrieve a paginated list of posts.
    The number of pages and items per page can be specified through query parameters.
    If not provided, defaults to page 1 and 20 items per page.

    **Parameters**:
    - request (`HttpRequest`): The HTTP request containing the user's authentication token
                            and optional query parameters for pagination.

    **Query Parameters:**
    - pages (`int`): Number of pages to retrieve (default: 1).
    - items_per_page (`int`): Number of posts per page (default: 20).

    **Responses:**
    - 200 OK: Returns a paginated list of posts and whether there are more pages to load.
    - 400 Bad Request: If the provided input for pages or items_per_page is invalid.

    **Example response on success:**

    {
    'posts': [
        {
        'id': 1,
        'author': {
            'id': 1,
            'email': 'some_user@mail.com'
        },
        'content': 'Some content.',
        'created_at': '2024-06-30T14:06:59.700338Z',
        'liked_users': []
        }
    ],
    'has_next': true
    }

    **Example response on error:**

    {
        'error': 'Invalid input for pages or items per page'
    }
    """

    pages = request.GET.get('pages', 1)
    items_per_page = request.GET.get('items_per_page', 20)

    try:
        pages, items_per_page = int(pages), int(items_per_page)

    except ValueError:
        return Response(
            {'error': 'Invalid input for pages or items per page'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    posts, has_next = get_all_posts(pages, items_per_page)

    # serialize from Django db Model instance to native Python data types
    posts_serialized = PostSerializer(posts, many=True).data

    data = {
        'posts': posts_serialized,
        'has_next': has_next,
    }

    return Response(data)  # Response() handles JSON rendering


@swagger_auto_schema(method='post', tags=['posts'], request_body=SubmitPostSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@log_activity
def submit_post(request):
    """
    post:
    Submit a new post with the provided data

    This endpoint allows an authenticated user to submit a new post. The request must
    include post content. Upon successful submission,
    the created post object is returned with a status of 201 Created.

    **Parameters**:
    - request (`HttpRequest`): The HTTP request containing the user's authentication token
                            and data to create the post.

    **Request Body**:
    - Content of the post.

    **Responses**:
    - 201 Created: Post successfully created. Returns the created post object.
    - 400 Bad Request: If post creation fails.

    **Example response on success:**

    {
    'id': 1,
    'author': {
        'id': 1,
        'email': 'some_user@mail.com'
    },
    'content': 'Some content.',
    'created_at': '2024-07-02T20:53:34.148889Z',
    'liked_users': []
    }

    **Example response on error:**

    {
        'title': ['This field is required.'],
        'content': ['This field is required.']
    }
    """

    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', tags=['posts'])
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@log_activity
def switch_like(request, post_id):
    """
    put:
    Toggle user's like status on a specific post

    The request must include the ID of the post as a path parameter in the URL.

    **Parameters**:
    - request (`HttpRequest`): The HTTP request containing the user's authentication token.
    - post_id (`int`): The ID of the post to switch the like status.

    **Responses**:
    - 201 Created: Like status switched successfully.
    - 404 Not Found: If the specified post ID does not exist.

    **Example response on success:**

    {
    'Post liked'
    }

    **Example response on error:**

    {
    'error': 'Post not found'
    }
    """

    try:
        res = switch_like_status(post_id, request.user)
        return Response(res, status=status.HTTP_201_CREATED)

    except PostNotFoundException as e:
        return Response({'error': e.message}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='delete', tags=['posts'])
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    """
    delete:
    Delete the specified post. Only the author of the post can delete it

    This endpoint allows an authenticated user who is the author of the post to delete it.
    The request must include the ID of the post in the URL.

    The endpoint marks the post as deleted and triggers a background task which
    hard deletes all posts that were removed 10+ days ago.

    **Parameters:**
    - request (`HttpRequest`): The HTTP request containing the user's authentication token.
    - post_id (`int`): The ID of the post to delete.

    **Responses:**
    - 204 No Content: Post deleted successfully.
      This response has no content.

    - 404 Not Found: If the specified post ID does not exist.
    - 403 Forbidden: If the authenticated user is not the author of the post.

    **Example response on success:**

    HTTP 204 No Content

    **Example response on error (post not found):**

    {
        'error': 'Post not found'
    }

    **Example response on error (unauthorized access):**

    {
    'error': 'Owner required'
    }
    """

    try:
        remove_post(post_id, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    except PostNotFoundException as e:
        return Response({'error': e.message}, status=status.HTTP_404_NOT_FOUND)

    except UnauthorizedAccessException as e:
        return Response({'error': e.message}, status=status.HTTP_403_FORBIDDEN)
