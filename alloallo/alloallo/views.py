from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from alloallo.accounts.models import User
from alloallo.accounts.forms import SearchForm


class HomePage(generic.TemplateView):
    template_name = "home.html"


class AboutPage(generic.TemplateView):
    template_name = "about.html"


class FindFriend(generic.FormView):
    template_name = "alloallo/find_friend.html"
    form_class = SearchForm

    def get(self, request):
        friend = request.GET.get('friend')
        if friend:
            return HttpResponseRedirect(
                reverse('profiles:show', kwargs={'pk': friend}))
        else:
            return super(FindFriend, self).get(request)


class Friends(generic.ListView):
    template_name = "alloallo/friends.html"
    model = User
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.friends.all()
