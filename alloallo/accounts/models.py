from __future__ import unicode_literals

import braintree

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

        user.create_customer_id()

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
    is_paid = models.BooleanField(
        _("paid"), default=False,
        help_text=_("Whether the user has paid for their account. Unpaid"
                    " accounts can't use the service."))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    friends = models.ManyToManyField('accounts.User')

    objects = UserManager()

    bt_customer_id = models.IntegerField(null=True)

    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['number']

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.number

    def create_customer_id(self):
        """
        Create a Braintree customer id
        """
        if self.bt_customer_id and self.bt_customer_id > 0:
            return
        result = braintree.Customer.create({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.number,
        })
        if result.is_success:
            self.bt_customer_id = result.customer.id
        else:
            raise ValueError("Braintree failed to create customer identity. Please check user details.")

    def get_client_token(self):
        # Make sure we have a customer id
        if self.bt_customer_id < 1:
            self.create_customer_id()
            self.save()
        return braintree.ClientToken.generate({
            "customer_id": self.bt_customer_id,
        })

    @python_2_unicode_compatible
    def __str__(self):
        return self.get_full_name()
