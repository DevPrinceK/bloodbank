from django.shortcuts import redirect, render
from django.views import View


class HomePageView(View):
    '''Home page view - renders the landing page'''
    template = 'website/home.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)
