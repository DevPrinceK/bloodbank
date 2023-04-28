import array
from core import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
import requests

from .models import BloodRequest, PatientProfile
from accounts.models import User


@receiver(post_save, sender=BloodRequest)
def notify_patient(sender, instance, created, **kwargs):
    if not created:
        sender = settings.SMS_SENDER
        numbers = [str(instance.patient_profile.user.phone), str(instance.patient_profile.phone)]  # noqa
        if instance.status == "APPROVED":
            message = f"Hello {instance.patient_profile.user.fullname}, \nWe are happy to let you know that your request {instance.blood_request_id} for {instance.patient_profile.blood_type} blood has been approved. Please visit the hospital to get your blood."
        elif instance.status == "REJECTED":
            message = f"Hello {instance.patient_profile.user.fullname}, \nWe are sorry to let you know that your request {instance.blood_request_id} for {instance.patient_profile.blood_type} blood has been rejected. Please request again with doctor's permit of request."
        try:
            send_sms(sender, message, numbers)  # noqa
        except Exception as e:
            print(e)
        else:
            print('SMS sent successfully')


@receiver(post_save, sender=User)
def add_patient_to_group(sender, instance, created, **kwargs):
    if instance.is_patient:
        # check if user has any group already that contains patient
        if instance.groups.filter(name__icontains='patient').exists():
            print('User already in patient group')
            return
        # search for patient group
        group = Group.objects.filter(
            Q(name__icontains='patient')
        ).first()
        # add user to group if group exists
        if group:
            instance.groups.add(group)
            instance.save()
            print('User added to patient group')


def send_sms(sender: str, message: str, recipients: array.array):
    header = {"api-key": settings.ARKESEL_API_KEY, 'Content-Type': 'application/json',
              'Accept': 'application/json'}
    SEND_SMS_URL = "https://sms.arkesel.com/api/v2/sms/send"
    payload = {
        "sender": sender,
        "message": message,
        "recipients": recipients
    }
    response = requests.post(SEND_SMS_URL, headers=header, json=payload)
    print(response.json())
    return response.json()
