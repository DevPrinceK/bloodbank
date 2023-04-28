from django.contrib import messages
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View

from accounts.models import User
from core.utils.decorators import AdminOnly, MustLogin
from dashboard.forms import UserForm


class UsersListView(PermissionRequiredMixin, View):
    '''CBV for User list page'''
    permission_required = ['accounts.view_user']

    template = 'dashboard/users.html'

    # @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        users = User.objects.all().order_by('-id')
        context = {
            'users': users,
            'total_users': users.count(),
        }
        return render(request, self.template, context)


class CreateUpdateUserView(PermissionRequiredMixin, View):
    '''CBV for Create and Update User'''
    permission_required = [
        'accounts.add_user',
        'accounts.change_user'
    ]

    template = 'dashboard/form-renderers/create_update_user.html'

    # @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        user = User.objects.filter(id=user_id).first()
        groups = Group.objects.all().order_by('name')
        if user:
            head = "Update"
        else:
            head = "Create"
        context = {
            'user': user,
            'groups': groups,
            'head': head,

        }
        return render(request, self.template, context)

    # @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id') or None
        account_status = request.POST.get('account_status')
        group_ids = request.POST.getlist('groups')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        user = User.objects.filter(id=user_id).first()
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            if not user:
                if password != password2:
                    messages.error(request, 'Passwords Do Not Match')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                user = form.save(commit=False)
                if account_status == '1':
                    user.is_staff = True
                    user.is_patient = False
                else:
                    user.is_staff = False
                    user.is_patient = True
                user.set_password(password)
                user.save()
                user.groups.clear()
                for group_id in group_ids:
                    group = Group.objects.filter(id=group_id).first()
                    user.groups.add(group)
                messages.success(request, 'User Created Successfully')
                return redirect('dashboard:users')
            user = form.save(commit=False)
            if account_status == '1':
                user.is_staff = True
                user.is_patient = False
            else:
                user.is_staff = False
                user.is_patient = True
            user.save()
            user.groups.clear()
            for group_id in group_ids:
                group = Group.objects.filter(id=group_id).first()
                user.groups.add(group)
            messages.success(request, 'User Updated successfully')
            return redirect('dashboard:users')
        else:
            for k, v in form.errors.items():
                print(k, v)
                messages.info(request, f'{k}: {v}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SearchUserView(PermissionRequiredMixin, View):
    '''CBV for searching Users'''
    permission_required = ['accounts.view_user']

    template = 'dashboard/users.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        users = User.objects.filter(
            Q(fullname__icontains=query) |
            Q(email__icontains=query)
        ).order_by('-id')
        context = {
            'users': users,
            'total_users': users.count(),
            'search': True,
        }
        return render(request, self.template, context)


class DeleteUserView(PermissionRequiredMixin, View):
    '''CBV for deleting User'''
    permission_required = ['accounts.delete_user']

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if user == request.user:
            messages.info(request, 'You Cannot Delete Yourself')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if user:
            user.delete()
            messages.success(request, 'User Deleted Successfully')
            return redirect('dashboard:users')
        messages.error(request, 'User Does Not Exist')
        return redirect('dashboard:users')


class AddUserToGroupsView(PermissionRequiredMixin, View):
    '''CBV for adding user to groups'''
    permission_required = [
        'accounts.add_user_to_group',
    ]

    template = 'dashboard/details/details_user_permissions.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id') or None
        user = User.objects.filter(id=user_id).first()
        groups = Group.objects.all().order_by('name')
        if user:
            permissions = Permission.objects.all().order_by('name')
            saved_permissions = user.user_permissions.all()
            saved_groups = user.groups.all()
            context = {
                'user': user,
                'permissions': permissions,
                'saved_groups': saved_groups,
                'groups': groups,
                'saved_permissions': saved_permissions,
            }
            return render(request, self.template, context)  # noqa
        messages.info(request, 'User Does Not Exist')
        return redirect('dashboard:users')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id') or None
        user = User.objects.filter(id=user_id).first()
        user_groups = request.POST.getlist('groups')
        if user:
            user.groups.clear()
            for group in user_groups:
                item = Group.objects.filter(id=group).first()
                user.groups.add(item)
            user.save()
            messages.success(request, 'User Groups Updated Successfully')  # noqa
        else:
            messages.info(request, 'User Does Not Exist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddPermsToUserView(PermissionRequiredMixin, View):
    '''CBV for assigning permissinos to user'''
    permission_required = [
        'accounts.add_permission_to_user',
    ]

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:add_user_to_group')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id') or None
        user = User.objects.filter(id=user_id).first()
        user_permissions = request.POST.getlist('permissions')
        if user:
            user.user_permissions.clear()
            for permission in user_permissions:
                item = Permission.objects.filter(id=permission).first()
                user.user_permissions.add(item)
            user.save()
            messages.success(request, 'User Permissions Updated Successfully')  # noqa
        else:
            messages.info(request, 'User Does Not Exist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
