from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .manager import UserManager
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError


RESERVED_USERNAMES = ["admin", "support", "help"]


def validate_username(value):
    if value.lower() in RESERVED_USERNAMES:
        raise ValidationError(f'The username "{value}" is reserved and cannot be used.')


def validate_non_numeric_username(value):
    if value.isdigit():
        raise ValidationError("Username cannot be entirely numeric.")


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_.-]+$",
                message="Username can only contain letters, numbers, and ./-/_ characters.",
            ),
            MinLengthValidator(3),
            validate_username,
            validate_non_numeric_username,
        ],
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
            "Unselect this instead of deleting accounts."
        ),
    )
    is_active = models.BooleanField(_("Is Active"), default=True)
    date_created = models.DateTimeField(_("date created"), default=timezone.now)

    USERNAME_FIELD = "username"

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.username = self.username.strip().lower()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "users"
