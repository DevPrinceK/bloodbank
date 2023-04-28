from django.contrib import messages
from django.shortcuts import redirect


class MustLogin(object):
    '''Decorator to check if user is logged in'''

    def __init__(self, original_method):
        self.original_method = original_method

    def __call__(self, request, *args,  **kwargs):
        if request.user.is_authenticated:
            return self.original_method(request, *args, **kwargs)
        else:
            messages.info(request, 'Please Login!.')  # noqa
            return redirect('accounts:login')


class AdminOnly(object):
    '''Decorator to check if logged-in user is an admin'''

    def __init__(self, original_method):
        self.original_method = original_method

    def __call__(self, request, *args,  **kwargs):
        if request.user.is_authenticated:
            if (request.user.is_superuser):  # noqa
                return self.original_method(request, *args, **kwargs)
            else:
                messages.info(request, "Access Denied!")  # noqa
                return redirect('accounts:login')
        else:
            messages.info(request, 'Please Login!')  # noqa
            return redirect('accounts:login')
