from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from django_blockstack.profile import fetch_profile


class HomePageView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return context
        context['profile'] = fetch_profile(self.request.user.username)
        try:
            for image in context['profile']['claim']['image']:
                if image['name'] in ['cover', 'avatar']:
                    context[image['name']] = image['contentUrl']
            for proof in context['profile']['claim']['account']:
                if proof['service'] in ['github', 'facebook', 'twitter']:
                    context[proof['service']] = proof
        except KeyError:
            pass
        return context


def sign_out(request):
    logout(request)
    return redirect('home')
