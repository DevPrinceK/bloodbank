from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from core.utils.decorators import MustLogin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from dashboard.models import Donation, Donor
from dashboard.forms import DonationForm


class DonationsListView(PermissionRequiredMixin, View):
    '''Class for showing the list of Donations'''
    permission_required = ['dashboard.view_donation']

    template = 'dashboard/donations.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all().order_by('-created_at')
        context = {
            'donations': donations,
        }
        return render(request, self.template, context)


class CreateUpdateDonationView(PermissionRequiredMixin, View):
    '''Class for creating and updating donations'''
    permission_required = ['dashboard.add_donation']
    template = 'dashboard/form-renderers/create_update_donation.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        donation_id = request.GET.get('donation_id') or None
        donation = Donation.objects.filter(id=donation_id).first()
        donors = Donor.objects.all().order_by('-id')
        context = {
            'donation': donation,
            'donors': donors,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        donation_id = request.POST.get('donation_id') or None
        donation = Donation.objects.filter(id=donation_id).first()
        donor_id = request.POST.get('donor_id') or None
        donor = Donor.objects.filter(id=donor_id).first()
        donation_form = DonationForm(request.POST, instance=donation)
        if donation_form.is_valid():
            donation = donation_form.save(commit=False)
            donation.donor = donor
            donation.save()
            if donation_id:
                messages.success(request, 'Donation Updated Successfully')
                return redirect('dashboard:donations')
            else:
                messages.success(request, 'Donation Saved Successfully')
                return redirect('dashboard:donations')
        else:
            for k, v in donation_form.errors.items():
                messages.info(request, f'{k}: {v}')
                return redirect('dashboard:donations')


class SearchDonationView(PermissionRequiredMixin, View):
    '''Class for searching Donation'''
    permission_required = ['dashboard.view_donation']

    template = 'dashboard/donations.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        donations = Donation.objects.filter(
            Q(donor__blood_type__icontains=query) |
            Q(donation_id__icontains=query) |
            Q(donor__email__icontains=query) |
            Q(donor__fullname__icontains=query)
        ).order_by('-created_at')
        context = {
            'donations': donations,
        }
        return render(request, self.template, context)


class DeleteDonationView(PermissionRequiredMixin, View):
    '''Class for deleting Donations'''
    permission_required = ['dashboard.delete_donation']

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:donations')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        donation_id = request.POST.get('donation_id')
        donation = Donation.objects.filter(id=donation_id).first()
        if donation:
            donation.delete()
            messages.success(request, 'Donation Deleted successfully')
        else:
            messages.info(request, 'Donation Does Not Exist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
