
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View

from core.utils.decorators import MustLogin


class ProfileView(PermissionRequiredMixin, View):
    '''CBV for profile page'''
    permission_required = [
        'accounts.view_profile',
    ]

    template = 'dashboard/profile.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        context = {
        }
        return render(request, self.template, context)


class ProfileUpdateView(PermissionRequiredMixin, View):
    '''CBV for profile update page'''
    permission_required = [
        'accounts.view_profile',
        'accounts.change_profile',
    ]

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:profile')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        user = request.user
        user.fullname = request.POST.get('fullname')
        user.phone = request.POST.get('phone')
        user.gender = request.POST.get('gender')
        if request.FILES.get('profile_image'):
            try:
                user.profile_image = request.FILES.get('profile_image')
            except:
                print('Error while uploading profile image')
            else:
                print('Profile image uploaded successfully')
        user.save()
        messages.success(request, 'Profile Updated successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PasswordResetView(PermissionRequiredMixin, View):
    '''CBV for password reset page'''
    permission_required = [
        'accounts.view_profile',
        'accounts.change_profile',
        'accounts.reset_password',
    ]

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:profile')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        password1 = request.POST.get('new_password')
        password2 = request.POST.get('confirm_password')
        if password1 == password2:
            user = request.user
            user.set_password(password1)
            user.save()
            messages.success(request, 'Password Changed successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request, 'Password does not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
