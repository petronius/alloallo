from __future__ import unicode_literals

from authtools.models import UserManager

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, number, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not number:
            raise ValueError('Users must have an email address')

        user = self.model(number=number)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, number, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(number, password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    number = models.CharField(max_length=64, unique=True,
                              null=False, blank=False)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    email = models.CharField(max_length=256, null=True, blank=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active.  Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['number']

    def get_full_name(self):
        return self.number

    def get_short_name(self):
        return self.number

    @python_2_unicode_compatible
    def __str__(self):
        return self.number
