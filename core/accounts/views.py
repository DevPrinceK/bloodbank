from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View
from dashboard.forms import PatientProfileForm, UserForm


class LoginView(View):
    '''Class to handle user login'''
    template = 'accounts/login_signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f'Welcome, {user.get_fullname()}!')
            return redirect('dashboard:dashboard')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect("accounts:login")


class RegisterView(View):

    def get(self, request, *args, **kwargs):
        return redirect('accounts:login')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.info(request, 'Passwords do not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        user_form = UserForm(request.POST, request.FILES or None)
        patient_profile_form = PatientProfileForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(password)
            user.save()
            # create patient profile
            if patient_profile_form.is_valid():
                patient_profile = patient_profile_form.save(commit=False)
                patient_profile.user = user
                patient_profile.save()
                user.is_patient = True
                user.save()
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Welcome, {user.fullname}!')
                return redirect('dashboard:dashboard')
            else:
                messages.info(request, 'Invalid credentials')
                return redirect("accounts:login")
        else:
            for k, v in form.errors.items():
                messages.info(request, f'{k}: {v}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')
