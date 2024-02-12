from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from users.managers import CustomUserManager
from utils import UserRoleChoices


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=100,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and -/_ only.'),
        validators=[RegexValidator(regex="^[a-zA-Z0-9\-_ ]{4,100}$",
                                   message="Enter a valid username. This value may contain only letters, digits, -,_")],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    phone_number = models.CharField(unique=True, max_length=20)

    role = models.SmallIntegerField(choices=UserRoleChoices.choices, default=UserRoleChoices.VISITOR)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True
        db_table = 'users'

    def __str__(self) -> str:
        return self.username

class User(AbstractUser):

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'