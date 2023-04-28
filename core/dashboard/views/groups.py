from django.contrib import messages
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View

from core.utils.decorators import AdminOnly, MustLogin


class GroupsListView(PermissionRequiredMixin, View):
    '''CBV for Group list page'''
    permission_required = ['auth.view_group']

    template = 'dashboard/groups.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        groups = Group.objects.all().order_by('-id')
        context = {
            'groups': groups,
            'total_groups': groups.count(),
        }
        return render(request, self.template, context)


class CreateUpdateGroupView(PermissionRequiredMixin, View):
    '''CBV for creating and updating a group'''
    permission_required = [
        'auth.add_group',
        'auth.change_group'
    ]

    template = 'dashboard/form-renderers/create_update_group.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        group_id = request.GET.get('group_id') or None
        group = Group.objects.filter(id=group_id).first()
        permissions = Permission.objects.all().order_by('name')
        if group:
            head = "Update"
        else:
            head = "Create"
        context = {
            "head": head,
            'group': group,
            'permissions': permissions,
        }
        return render(request, self.template, context)

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        group_id = request.POST.get('group_id') or None
        group = Group.objects.filter(id=group_id).first()
        group_name = request.POST.get('name')
        if group:
            group.name = group_name
            group.save()
            messages.success(request, 'Group Updated Successfully')
        else:
            group = Group.objects.create(name=group_name)
            messages.success(request, f'{group.name.upper()} Group Created Successfully')  # noqa
        return redirect('dashboard:groups')


class SearchGroupView(PermissionRequiredMixin, View):
    '''CBV for searching a group'''
    permission_required = ['auth.view_group']

    template = 'dashboard/groups.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('q')
        groups = Group.objects.filter(
            Q(name__icontains=search_term)
        ).order_by('-id')
        context = {
            'groups': groups,
            'total_groups': groups.count(),
            'search': True,
        }
        return render(request, self.template, context)


class DeleteGroupView(PermissionRequiredMixin, View):
    '''CBV for deleting a group'''
    permission_required = ['auth.delete_group']

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:groups')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        group_id = request.POST.get('group_id') or None
        group = Group.objects.filter(id=group_id).first()
        if group:
            group.delete()
            messages.success(request, 'Group Deleted Successfully')
        else:
            messages.error(request, 'Group Does Not Exist')
        return redirect('dashboard:groups')


class AddPermissionsToGroupView(PermissionRequiredMixin, View):
    '''CBV for adding permissions to a group'''
    permission_required = [
        'auth.add_group',
        'auth.change_group',
        'auth.add_permission',
        'auth.change_permission'
    ]
    template = 'dashboard/details/details_permissions.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        group = request.GET.get('group_id') or None
        group = Group.objects.filter(id=group).first()
        if group:
            permissions = Permission.objects.all().order_by('name')
            saved_permissions = group.permissions.all()
            context = {
                'group': group,
                'permissions': permissions,
                'saved_permissions': saved_permissions,
            }
            print(group.permissions)
            return render(request, self.template, context)  # noqa
        messages.info(request, 'Group Does Not Exist')
        return redirect('dashboard:groups')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        group_id = request.POST.get('group_id') or None
        group = Group.objects.filter(id=group_id).first()
        group_permissions = request.POST.getlist('permissions')
        if group:
            group.permissions.clear()
            for permission in group_permissions:
                permission = Permission.objects.filter(id=permission).first()
                group.permissions.add(permission)
            group.save()
            messages.success(request, 'Group Permissions Updated Successfully')  # noqa
        else:
            messages.info(request, 'Group does not exist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
