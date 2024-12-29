from uuid import uuid4

import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from rest_framework.exceptions import AuthenticationFailed

from authentications.models import User


def save_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()
        return img_temp


def register_social_user(profile_image_url, provider, email, name, role) -> User:
    filtered_user = User.objects.filter(email=email)

    if len(filtered_user):

        if provider == filtered_user[0].oauth_provider:
            return filtered_user[0]

        else:
            raise AuthenticationFailed(
                detail="Please continue your login using "
                + filtered_user[0].oauth_provider
            )

    else:
        user = {
            "email": email,
            "oauth_provider": provider,
            "role": role,
            "is_verified": True,
        }
        user = User.objects.create_user(**user)
        user.user_information.full_name = name
        # Save profile picture from URL
        if profile_image_url:
            image_temp = save_image_from_url(profile_image_url)
            user.user_information.profile_picture.save(str(uuid4()), File(image_temp))
        user.user_information.save(update_fields=["full_name", "profile_picture"])

        return user
