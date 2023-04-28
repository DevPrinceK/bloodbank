from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from core.utils.constants import BloodType as BT
from core.utils.constants import Titles as T
from core.utils.decorators import MustLogin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from dashboard.models import Donor
from dashboard.forms import DonorForm


class DonorsListView(PermissionRequiredMixin, View):

    '''Class for showing the list of Donors'''
    permission_required = ['dashboard.view_department']

    template = 'dashboard/donors.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        donors = Donor.objects.all().order_by('-created_at')
        blood_types = BT.__members__.keys()
        titles = T.__members__.keys()
        context = {
            'donors': donors,
            'blood_types': blood_types,
            'titles': titles,
        }
        return render(request, self.template, context)


class CreateUpdateDonorView(PermissionRequiredMixin, View):
    '''Class for creating and updating a donor'''
    permission_required = ['dashboard.add_donor', 'dashboard.change_donor']

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:donors')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        donor_id = request.POST.get('donor_id')
        donor = Donor.objects.filter(id=donor_id).first()
        donor_form = DonorForm(request.POST, instance=donor)

        # donor exists - update
        if donor:
            if donor_form.is_valid():
                item = donor_form.save(commit=False)
                item.created_by = request.user
                item.save()
                messages.success(request, 'Donor updated successfully')
            else:
                for k, v in donor_form.errors.items():
                    print(k, v)
                    messages.info(request, f'{k}: {v}')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:  # create new donor
            donor_form = DonorForm(request.POST)
            if donor_form.is_valid():
                item = donor_form.save(commit=False)
                if not item.created_by:
                    item.created_by = request.user
                item.save()
                messages.success(request, 'Donor created successfully')
            else:
                for k, v in donor_form.errors.items():
                    print(k, v)
                    messages.info(request, f'{k}: {v}')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SearchDonorView(PermissionRequiredMixin, View):
    '''Class for searching donor'''
    permission_required = ['dashboard.view_donor']

    template = 'dashboard/donors.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        donors = Donor.objects.filter(
            Q(blood_type__icontains=query) |
            Q(address__icontains=query) |
            Q(phone__icontains=query) |
            Q(fullname__icontains=query) |
            Q(title__icontains=query) |
            Q(ocupation__icontains=query) |
            Q(medical_condition__icontains=query)
        ).order_by('-created_at')
        context = {
            'donors': donors,
        }
        return render(request, self.template, context)


class DeleteDonorView(PermissionRequiredMixin, View):
    '''Class for deleting Donors'''
    permission_required = ['dashboard.delete_donor']

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:donors')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        donor_id = request.POST.get('donor_id')
        donor = Donor.objects.filter(id=donor_id).first()
        if donor:
            donor.delete()
            messages.success(request, 'Donor deleted successfully')
        else:
            messages.info(request, 'Donor does not exist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
