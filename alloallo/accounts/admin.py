from __future__ import unicode_literals

import copy

from authtools.admin import NamedUserAdmin

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.forms import ModelForm
from django.core.urlresolvers import reverse

from alloallo.profiles.models import Profile
from alloallo.accounts.models import User


USERNAME_FIELD = User.USERNAME_FIELD

REQUIRED_FIELDS = (USERNAME_FIELD,) + tuple(User.REQUIRED_FIELDS)

BASE_FIELDS = (None, {
    'fields': REQUIRED_FIELDS + ('password', 'first_name', 'last_name', 'friends'),
})

SIMPLE_PERMISSION_FIELDS = (_('Permissions'), {
    'fields': ('is_active', 'is_staff', 'is_superuser',),
})

ADVANCED_PERMISSION_FIELDS = copy.deepcopy(SIMPLE_PERMISSION_FIELDS)
ADVANCED_PERMISSION_FIELDS[1]['fields'] += ('groups', 'user_permissions',)

DATE_FIELDS = (_('Important dates'), {
    'fields': ('last_login', 'date_joined',),
})


class UserProfileInline(admin.StackedInline):
    model = Profile


class UserAdminForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class NewUserAdmin(NamedUserAdmin):
    fieldsets = (
        BASE_FIELDS,
        ADVANCED_PERMISSION_FIELDS,
        DATE_FIELDS,
    )
    inlines = [UserProfileInline]
    list_display = ('is_active', 'first_name', 'number', 'permalink',
                    'is_superuser', 'is_staff',)
    list_display_links = ('first_name', 'number',)

    # 'View on site' didn't work since the original User model needs to
    # have get_absolute_url defined. So showing on the list display
    # was a workaround.
    def permalink(self, obj):
        url = reverse("profiles:show",
                      kwargs={"pk": obj.pk})
        # Unicode hex b6 is the Pilcrow sign
        return '<a href="{}">{}</a>'.format(url, '\xb6')
    permalink.allow_tags = True

admin.site.register(User, NewUserAdmin)