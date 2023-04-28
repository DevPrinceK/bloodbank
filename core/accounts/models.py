from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='profile_images', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    created_by_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_fullname(self):
        '''return the full name of the user'''
        return self.fullname if self.fullname else self.email

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def get_user_type_color(self) -> str:
        '''return the user type color'''
        if self.is_superuser:
            return 'danger'
        elif self.is_staff:
            return 'warning'
        else:
            return 'primary'

    def __str__(self):
        return self.get_fullname()

    class Meta:
        db_table = 'user'
        # custom permissions
        permissions = [
            ("view_profile", "Can view profile"),
            ("view_setting", "Can view setting"),
            ("change_profile", "Can update profile"),
            ("reset_password", "Can reset password"),
            ("add_user_to_group", "Can add user to group"),
            ("add_patient", "Can add patient"),
            ("change_patient", "Can update patient"),
            ("add_permission_to_user", "Can add permission to user"),
        ]
