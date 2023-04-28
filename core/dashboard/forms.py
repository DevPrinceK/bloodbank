from django import forms
from accounts.models import User
from dashboard.models import Donor, PatientProfile, Donation, BloodRequest


class UserForm(forms.ModelForm):
    '''Form for creating a new user'''
    class Meta:
        model = User
        fields = ['email', 'fullname', 'phone', 'gender', 'profile_image', ]


class PatientProfileForm(forms.ModelForm):
    '''Form for creating a new user profile'''
    class Meta:
        model = PatientProfile
        exclude = ['created_at', 'user', ]


class DonorForm(forms.ModelForm):
    '''Form for creating a new donor'''
    class Meta:
        model = Donor
        exclude = ['created_at', 'created_by', ]


class DonationForm(forms.ModelForm):
    '''Form for creating a new donation'''
    class Meta:
        model = Donation
        fields = ['date_time_donated', 'quantity', ]


class BloodRequestForm(forms.ModelForm):
    '''Form for creating a new blood request'''
    class Meta:
        model = BloodRequest
        fields = ['quantity', ]