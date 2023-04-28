from django.db import models
from accounts.models import User
from datetime import timedelta


class Donor(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(default="default@gmail.com")
    blood_type = models.CharField(max_length=15)
    dob = models.DateField()
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    medical_condition = models.CharField(max_length=500)
    title = models.CharField(max_length=10)
    ocupation = models.CharField(max_length=100)
    id_type = models.CharField(max_length=20)
    id_number = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.fullname


class Donation(models.Model):
    '''Model to store donation details'''
    def generate_donation_id():
        # method to generate a custom ID for donation object
        from .models import Donation
        count = Donation.objects.count()
        return 'DON-#-000' + str(Donation.objects.count() + 1)

    donor = models.ForeignKey('Donor', on_delete=models.CASCADE, null=True)
    donation_id = models.CharField(default=generate_donation_id, max_length=20)  # noqa
    date_time_donated = models.DateTimeField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def expiration_date(self) -> timedelta:
        '''return the expiration date of the blood'''
        expiration_date = self.date_time_donated + timedelta(days=40)
        return expiration_date

    def blood_is_expired(self) -> bool:
        '''check if the blood has expired'''
        expiration_date = self.date_time_donated + timedelta(days=40)
        today = timezone.now()
        return today > expiration_date

    def blood_expires_in_a_week_or_less(self) -> bool:
        '''check if the blood will expire in a week or less'''
        expiration_date = self.date_time_donated + timedelta(days=40)
        today = timezone.now()
        time_until_expiration = expiration_date - today
        return time_until_expiration <= timedelta(days=7)

    def __str__(self) -> str:
        return self.donation_id + ' - ' + self.donor.fullname if self.donor else 'No Donor'


class PatientProfile(models.Model):
    '''Model to store patient profile - A patient is a user'''
    blood_type = models.CharField(max_length=15)
    dob = models.DateField()
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.fullname if self.user else 'No User'


class BloodRequest(models.Model):
    '''Model to blood requests made by patients'''

    def generate_request_id():
        # method to generate a custom ID for blood request object
        count = BloodRequest.objects.count()
        return 'BREQ-#-000' + str(BloodRequest.objects.count() + 1)
    blood_request_id = models.CharField(default=generate_request_id, max_length=20)  # noqa
    patient_profile = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, null=True)  # noqa
    request_form = models.ImageField(upload_to='request_forms', null=True, blank=True)  # noqa
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, default='PENDING')
    date_requested = models.DateTimeField(auto_now_add=True)
    date_approve_rejected = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_status_color(self) -> str:
        if self.status.upper == 'PENDING':
            return 'green'
        elif self.status.upper == 'APPROVED':
            return 'blue'
        else:
            return 'red'

    def __str__(self) -> str:
        return self.blood_request_id + ' - ' + self.patient_profile.user.fullname

    class Meta:
        # custom permissions
        permissions = [
            ("change_request_status", "Can change blood request status"),
        ]
