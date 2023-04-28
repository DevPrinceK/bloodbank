from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from core.utils.decorators import MustLogin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from dashboard.models import BloodRequest, PatientProfile
# from datetime import timezone
import datetime


class BloodRequestsListView(PermissionRequiredMixin, View):
    '''Class for showing the list of BloodRequests'''
    permission_required = ['dashboard.view_bloodrequest']

    template = 'dashboard/blood_requests.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        user = request.user
        patient_profile = PatientProfile.objects.filter(user=user).first()
        if user.is_staff or user.is_superuser:
            blood_requests = BloodRequest.objects.all().order_by('-created_at')
        else:
            blood_requests = BloodRequest.objects.filter(patient_profile=patient_profile).order_by('-created_at')  # noqa
        context = {
            'blood_requests': blood_requests,
        }
        return render(request, self.template, context)


class CreateUpdateBloodRequestView(PermissionRequiredMixin, View):
    '''Class for creating and updating blood requests'''
    permission_required = ['dashboard.add_bloodrequest']

    template = 'dashboard/form-renderers/create_update_request.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        blood_request_id = request.GET.get('request_id') or None
        if blood_request_id:
            blood_request = BloodRequest.objects.filter(
                blood_request_id=blood_request_id).first()
            context = {
                'blood_request': blood_request,
            }
            return render(request, self.template, context)
        else:
            return render(request, self.template)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        blood_request_id = request.POST.get('request_id')
        quantity = request.POST.get('quantity')
        if blood_request_id:
            blood_request = BloodRequest.objects.filter(
                blood_request_id=blood_request_id).first()
            if blood_request:
                blood_request.quantity = quantity
                blood_request.save()
                messages.success(request, 'Blood Request Updated Successfully')
            else:
                messages.info(request, 'Blood Request Does Not Exist')
        else:
            # patient_profile = request.user.patient_profile
            patient_profile = PatientProfile.objects.filter(user=request.user).first()  # noqa
            blood_request = BloodRequest.objects.create(
                patient_profile=patient_profile,
                quantity=quantity,
            )
            messages.success(request, 'Blood Request Created Successfully')
        return redirect('dashboard:blood_requests')


class BloodRequestDetailsView(PermissionRequiredMixin, View):
    '''Class for viewing the details of blood requests'''
    permission_required = ['dashboard.view_bloodrequest']
    template = 'dashboard/details/details_blood_request.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        request_id = request.GET.get('request_id')
        blood_request = BloodRequest.objects.filter(id=request_id).first()  # noqa
        context = {
            'blood_request': blood_request,
        }
        return render(request, self.template, context)


class ChangeRequestStatusView(PermissionRequiredMixin, View):
    '''Class for changing the status of a blood request'''
    permission_required = [
        'dashboard.change_bloodrequest', 'change_request_status']

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:blood_requests')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        request_id = request.POST.get('request_id')
        status = request.POST.get('request_status')
        request_form = request.POST.get('request_form')
        blood_request = BloodRequest.objects.filter(id=request_id).first()
        if blood_request:
            blood_request.status = status
            # add request form if
            if request_form:
                blood_request.request_form = request_form
            blood_request.date_approve_rejected = datetime.datetime.now()
            blood_request.save()
            messages.success(request, 'Blood Request Status Changed Successfully')  # noqa
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request, 'Blood Request Does Not Exist')
            return redirect('dashboard:blood_requests')


class SearchBloodRequestView(PermissionRequiredMixin, View):
    '''Class for searching Blood Request'''
    permission_required = ['dashboard.view_bloodrequest']

    template = 'dashboard/blood_requests.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        blood_requests = BloodRequest.objects.filter(
            Q(blood_request_id__icontains=query) |
            Q(status__icontains=query) |
            Q(patient_profile__user__fullname__icontains=query)
        ).order_by('-created_at')
        context = {
            'blood_requests': blood_requests,
        }
        return render(request, self.template, context)


class DeleteBloodRequestView(PermissionRequiredMixin, View):
    '''Class for deleting blood requests'''
    permission_required = ['dashboard.delete_bloodrequest']

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:blood_requests')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        blood_request_id = request.POST.get('blood_request_id')
        blood_request = BloodRequest.objects.filter(
            id=blood_request_id).first()
        if blood_request:
            blood_request.delete()
            messages.success(request, 'Blood Request Deleted Successfully')
        else:
            messages.info(request, 'Blood Request Does Not Exist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
