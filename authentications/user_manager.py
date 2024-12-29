from django.contrib.auth.models import BaseUserManager
from django.db import transaction


class UserManager(BaseUserManager):
    """
    This is the manager for custom user model
    """

    @transaction.atomic
    def create_user(
        self, email, password=None, oauth_provider=None, role=None, is_verified=False
    ):

        if not role:
            raise ValueError("Role should not be empty")

        if not email:
            raise ValueError("Email should not be empty")

        if not oauth_provider:
            raise ValueError("oauth_provider should not be empty")

        if oauth_provider == "email" and not password:
            raise ValueError("Password should not be empty")

        if email:
            user = self.model(
                email=self.normalize_email(email=email),
                oauth_provider=oauth_provider,
                role=role,
            )
        else:
            user = self.model(oauth_provider=oauth_provider, role=role)

        user.is_verified = is_verified
        user.set_password(password)
        user.save(using=self._db)
        return user

    @transaction.atomic
    def create_superuser(
        self, email, password=None, oauth_provider="email", role="admin"
    ):
        if not password:
            raise ValueError("Password should not be empty")

        user = self.create_user(
            email=email,
            password=password,
            oauth_provider=oauth_provider,
            role=role,
            is_verified=True,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
