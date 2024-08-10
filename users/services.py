import os
from django.forms import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Sum
from django.core.exceptions import SuspiciousFileOperation

from posts.models import Post


ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png']


def create_user(serializer, email, password) -> bool:
    try:
        with transaction.atomic():
            user = serializer.save()
            user.set_password(password)
            user.username = email.split('@')[0] + str(user.id)
            user.is_sandboxed = True
            user.save()
        return True

    except IntegrityError:
        return False


def upload_profile_picture(profile_picture, user) -> None:
    if profile_picture:
        if profile_picture.content_type not in ALLOWED_IMAGE_TYPES:
            raise ValidationError('Only JPEG and PNG images are allowed.')

        try:
            file_path = os.path.join('uploads', profile_picture.name)
            with open(os.path.join('media', file_path), 'wb+') as destination:
                for chunk in profile_picture.chunks():
                    destination.write(chunk)

            user.profile_picture = file_path
            user.save()

        except (IOError, SuspiciousFileOperation) as e:
            raise ValidationError(f'Failed to upload file: {e}')


def get_total_likes_and_posts(user) -> tuple[int]:
    user_id = user.id
    all_user_posts = Post.objects.filter(author_id=user_id)
    all_user_posts_likes = all_user_posts.aggregate(total_likes=Sum('likes'))

    return all_user_posts_likes, all_user_posts.count()
