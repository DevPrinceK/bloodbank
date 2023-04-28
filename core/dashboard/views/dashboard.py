import datetime
from datetime import timedelta, timezone
from django.utils import timezone as tz
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View
from dashboard.models import Donation, Donor, PatientProfile, BloodRequest
from django.db.models import Count, Sum, F, FloatField
from core.utils.decorators import MustLogin
from django.utils.decorators import method_decorator


class DashboardView(View):
    '''CBV for rendering the dashboard page'''

    template = 'dashboard/dashboard.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        # expired bloods
        expired_blood_count = Donation.objects.filter(
            date_time_donated__lte=tz.now()-timedelta(days=40)).count()
        # bloods expiring in a week or less
        expiring_blood_count = Donation.objects.filter(date_time_donated__gt=tz.now(
        )-timedelta(days=40), date_time_donated__lte=tz.now()+timedelta(days=7)).count()
        # messages
        message = f'{expired_blood_count} quantum of blood has expired | {expiring_blood_count} quantum of blood will expire in a week or less'  # noqa
        blood_types = Donation.objects.values_list('donor__blood_type', flat=True).distinct()  # noqa
        blood_type_counts = Donation.objects.values('donor__blood_type').annotate(count=Count('donor__blood_type'))  # noqa

        # get the total quantity of each blood type in the Donation model
        blood_type_totals = Donation.objects.values(
            'donor__blood_type').annotate(total_quantity=Sum('quantity'))

        # get the total quantity of each blood type requested in the BloodRequest model
        blood_type_requests = BloodRequest.objects.filter(status__in=['PENDING', 'REJECTED']).values(
            'patient_profile__blood_type').annotate(requested_quantity=Sum('quantity'))

        # combine the above queries to get the final result
        blood_type_info = []
        for blood_type in set(blood_type_totals.values_list('donor__blood_type', flat=True)):

            total_quantity = blood_type_totals.filter(
                donor__blood_type=blood_type).aggregate(Sum('quantity'))['quantity__sum']

            requested_quantity = blood_type_requests.filter(
                patient_profile__blood_type=blood_type).aggregate(Sum('quantity'))['quantity__sum']

            approve_requested_quantity = blood_type_requests.filter(
                patient_profile__blood_type=blood_type, status='APPROVED').aggregate(Sum('quantity'))['quantity__sum']

            available_quantity = float(
                total_quantity) - float(approve_requested_quantity or 0)

            blood_type_info.append({
                'blood_type': blood_type,
                'total_quantity': str(total_quantity or 0),
                'requested_quantity': str(requested_quantity or 0),
                'approve_requested_quantity': str(approve_requested_quantity or 0),
                'available_quantity': str(available_quantity)
            })

        # only display messages blood expiration message to staff and superusers
        if request.user.is_staff or request.user.is_superuser:
            messages.info(request, message)
        request_history = BloodRequest.objects.filter(
            patient_profile__user=request.user).order_by('-blood_request_id')

        context = {
            'blood_types': blood_types,
            'blood_type_counts': blood_type_counts,
            'blood_type_info': blood_type_info,
            'request_history': request_history,
        }

        return render(request, self.template, context)
