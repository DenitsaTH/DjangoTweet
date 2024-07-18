from django.core.paginator import Paginator
from django.utils import timezone

from posts.models import Post
from exceptions import PostNotFoundException, UnauthorizedAccessException


def get_post(id) -> Post | None:

    try:
        post = Post.objects.get(id=id)
        return post
    except Post.DoesNotExist:
        return


def is_user_owner(post, user) -> bool:
    return post.author == user


def switch_like_status(post_id, user) -> str:

    post = get_post(post_id)

    if not post:
        raise PostNotFoundException()

    if user in post.likes.all():
        post.likes.remove(user)
        return 'Post unliked'

    post.likes.add(user)
    return 'Post liked'


def remove_post(post_id, user) -> None:
    post = get_post(post_id)

    if not post:
        raise PostNotFoundException()

    if not is_user_owner(post, user):
        raise UnauthorizedAccessException()

    post.is_deleted = True
    post.deleted_at = timezone.now()
    post.save()


def get_all_posts(pages, items_per_page) -> tuple[list[Post], bool]:

    # QuerySets are lazy - no db interaction is made until they are evaluated
    all_posts = Post.objects.filter(is_deleted=False).order_by('-id')
    paginator = Paginator(all_posts, items_per_page)

    page_obj = paginator.get_page(pages)
    has_next = page_obj.has_next()
    posts = list(page_obj)

    return posts, has_next
