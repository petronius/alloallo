from __future__ import unicode_literals
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from alloallo.accounts.models import User
from braces.views import LoginRequiredMixin

from . import forms
from . import models


class ShowProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/show_profile.html"
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            user = get_object_or_404(User, pk=pk)
        else:
            user = self.request.user

        if user == self.request.user:
            kwargs["editable"] = True
        kwargs["show_user"] = user
        kwargs['pk'] = user.pk
        return super(ShowProfile, self).get(request, *args, **kwargs)

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        request.user.friends.add(user)
        messages.success(request, "User has been added to your friends.")

        return self.get(request, pk, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ShowProfile, self).get_context_data(**kwargs)
        ctx['can_add_as_friend'] = \
            self.request.user.friends.filter(pk=kwargs['pk']).count() <= 0
        return ctx


class EditProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/edit_profile.html"
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if "user_form" not in kwargs:
            kwargs["user_form"] = forms.UserForm(instance=user)
        if "profile_form" not in kwargs:
            kwargs["profile_form"] = forms.ProfileForm(instance=user.profile)
        return super(EditProfile, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_form = forms.UserForm(request.POST, instance=user)
        profile_form = forms.ProfileForm(request.POST,
                                         request.FILES,
                                         instance=user.profile)
        if not (user_form.is_valid() and profile_form.is_valid()):
            messages.error(request, "There was a problem with the form. "
                           "Please check the details.")
            user_form = forms.UserForm(instance=user)
            profile_form = forms.ProfileForm(instance=user.profile)
            return super(EditProfile, self).get(request,
                                                user_form=user_form,
                                                profile_form=profile_form)
        # Both forms are fine. Time to save!
        user_form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        messages.success(request, "Profile details saved!")
        return redirect("profiles:show_self")
