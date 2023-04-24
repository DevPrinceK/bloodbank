from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    '''manages User account creation'''

    def create_user(self, email, password, fullname='-', **kwargs):
        user = self.model(email=email, password=password,
                          fullname=fullname, **kwargs)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.is_patient = False
        user.save()
        return user

    def create_patient(self, email, password, fullname='-', **kwargs):
        user = self.model(email=email, password=password,
                          fullname=fullname, **kwargs)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.is_patient = True
        user.save()
        return user

    def create_staff(self, email, password, fullname='-', **kwargs):
        user = self.model(email=email, password=password,
                          fullname=fullname, **kwargs)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = False
        user.is_patient = False
        user.save()
        return user

    def create_superuser(self, email, password, fullname='-', **kwargs):
        user = self.create_user(
            email,  password, fullname='-', **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.created_from_app = False
        user.created_from_admin_panel = True
        user.save()
        return user
