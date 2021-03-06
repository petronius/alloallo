from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('number'),
        )

    class Meta:
        model = User
        fields = ['number', 'first_name', 'last_name']


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('picture'),
            Field('bio'),
            Submit('update', 'Update', css_class="btn-success"),
        )

    class Meta:
        model = models.Profile
        fields = ['picture', 'bio', 'is_available_for_random']
