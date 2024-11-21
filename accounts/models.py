from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class AccountConnection(models.Model):
    follower = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="following_connections",
        related_query_name="following_connection",
    )
    following = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="follower_connections",
        related_query_name="follower_connection",
    )
    is_request_accepted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="unique_connection"
            )
        ]
