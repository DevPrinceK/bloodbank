from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from core.utils.decorators import MustLogin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from dashboard.models import PatientProfile
from accounts.models import User
from dashboard.forms import PatientProfileForm, UserForm


class PatientsListView(PermissionRequiredMixin, View):
    '''Class for showing the list of patients'''
    permission_required = ['dashboard.view_patientprofile']
    template = 'dashboard/patients.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        patients = PatientProfile.objects.all().order_by('-id')
        context = {
            'patients': patients,
        }
        return render(request, self.template, context)


class CreateUpdatePatientView(PermissionRequiredMixin, View):
    '''Class for creating and updating a patient - user and patientprofile'''
    permission_required = ['accounts.add_patient', 'accounts.change_patient']
    template = 'dashboard/form-renderers/create_update_patient.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        patient_id = request.GET.get('patient_id')
        patient = PatientProfile.objects.filter(id=patient_id).first()
        context = {
            'patient': patient,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request):
        patient_id = request.POST.get('patient_id') or None
        user_id = request.POST.get('user_id') or None
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.info(request, 'Passwords Do Not Match!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # check if user/patient account exists
        user_item = User.objects.filter(id=user_id).first()
        patient_item = PatientProfile.objects.filter(id=patient_id).first()
        user_form = UserForm(request.POST, request.FILES or None, instance=user_item)  # noqa
        patient_profile_form = PatientProfileForm(request.POST, instance=patient_item)  # noqa
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
                if patient_item and user_item:
                    messages.info(request, 'Patient Account Updated Successfully!')  # noqa
                    return redirect('dashboard:patients')
                else:
                    messages.info(request, 'Patient Account Created Successfully!')  # noqa
                    return redirect('dashboard:patients')
            else:
                for k, v in patient_profile_form.errors.items():
                    messages.info(request, f'{k}: {v}')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            for k, v in user_form.errors.items():
                messages.info(request, f'{k}: {v}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SearchPatientView(PermissionRequiredMixin, View):
    '''Class for searching patients'''
    permission_required = ['dashboard.view_patientprofile']
    template = 'dashboard/patients.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        patients = PatientProfile.objects.filter(
            Q(blood_type__icontains=query) |
            Q(address__icontains=query) |
            Q(phone__icontains=query) |
            Q(user__fullname__icontains=query) |
            Q(user__email__icontains=query)
        ).order_by('-created_at')
        context = {
            'patients': patients,
        }
        return render(request, self.template, context)


class DeletePatientView(PermissionRequiredMixin, View):
    '''Class for deleting patients'''
    permission_required = ['dashboard.delete_patientprofile']

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:patients')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        patient_id = request.POST.get('patient_id')
        patient = PatientProfile.objects.filter(id=patient_id).first()
        if patient:
            patient.delete()
            messages.success(request, 'Patient deleted successfully')
        else:
            messages.info(request, 'Patient does not exist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
