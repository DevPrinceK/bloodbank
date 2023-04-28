from django.contrib import admin
from .models import Donor, Donation, BloodRequest, PatientProfile

admin.site.register(Donor)
admin.site.register(Donation)
admin.site.register(BloodRequest)
admin.site.register(PatientProfile)
