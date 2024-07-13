import os
from posts.models import Post
from users.models import User
from django.db import IntegrityError, transaction


def create_user(serializer, email, password) -> bool:

    try:
        with transaction.atomic():
            serializer.save()
        user = User.objects.get(email=email)
    except IntegrityError:
        return False
    else:
        user.set_password(password)
        user.username = email.split('@')[0] + str(user.id)
        user.is_sandboxed = True
        user.save()
        return True


def upload_profile_picture(profile_picture, user) -> None:
    
    if profile_picture:
        file_path = os.path.join('uploads', profile_picture.name)
        with open(os.path.join('media', file_path), 'wb+') as destination:
            for chunk in profile_picture.chunks():
                destination.write(chunk)

        user.profile_picture = file_path
        user.save()


def get_total_likes_and_posts(user) -> tuple[int]:
    user_id = user.id
    posts = Post.objects.filter(author_id=user_id)
    likes = sum(post.likes.count() for post in posts)

    return likes, len(posts)
