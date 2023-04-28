from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
]

# for patients
urlpatterns += [
    path('patients/', views.PatientsListView.as_view(), name='patients'),
    path('create-update-patient/',
         views.CreateUpdatePatientView.as_view(), name='create_update_patient'),
    path('search-patient/', views.SearchPatientView.as_view(), name='search_patient'),  # noqa
    path('delete-patient/', views.DeletePatientView.as_view(), name='delete_patient'),  # noqa
]

# for donors
urlpatterns += [
    path('donors/', views.DonorsListView.as_view(), name='donors'),
    path('create-update-donor/', views.CreateUpdateDonorView.as_view(),
         name='create_update_donor'),
    path('search-donor/', views.SearchDonorView.as_view(), name='search_donor'),
    path('delete-donor/', views.DeleteDonorView.as_view(), name='delete_donor'),
]

# for donations
urlpatterns += [
    path('donations/', views.DonationsListView.as_view(), name='donations'),
    path('create-update-donation/', views.CreateUpdateDonationView.as_view(), name='create_update_donation'),  # noqa
    path('search-donation/', views.SearchDonationView.as_view(), name='search_donation'),  # noqa
    path('delete-donation/', views.DeleteDonationView.as_view(), name='delete_donation'),  # noqa
]

# for blood requests
urlpatterns += [
    path('blood-requests/', views.BloodRequestsListView.as_view(), name='blood_requests'),  # noqa
    path('create-update-blood-request/', views.CreateUpdateBloodRequestView.as_view(), name='create_update_blood_request'),  # noqa
    path('blood-request-detail/', views.BloodRequestDetailsView.as_view(), name='blood_request_detail'),  # noqa
    path('search-blood-request/', views.SearchBloodRequestView.as_view(), name='search_blood_request'),  # noqa
    path('change-request-status/', views.ChangeRequestStatusView.as_view(), name='change_request_status'),  # noqa
    path('delete-blood-request/', views.DeleteBloodRequestView.as_view(), name='delete_blood_request'),  # noqa
]


# Users
urlpatterns += [
    path("users/", views.UsersListView.as_view(), name="users"),
    path("create-update-user/", views.CreateUpdateUserView.as_view(), name="create_update_user"),  # noqa
    path("search-user/", views.SearchUserView.as_view(), name="search_user"),  # noqa
    path("delete-user/", views.DeleteUserView.as_view(), name="delete_user"),  # noqa
    path("add-user-to-group/", views.AddUserToGroupsView.as_view(), name="add_user_to_group"),  # noqa
    path("add-perms-to-user/", views.AddPermsToUserView.as_view(), name="add_perms_to_user"),  # noqa
]

# Groups
urlpatterns += [
    path("groups/", views.GroupsListView.as_view(), name="groups"),
    path("create-update-group/", views.CreateUpdateGroupView.as_view(), name="create_update_group"),  # noqa
    path("search-group/", views.SearchGroupView.as_view(), name="search_group"),  # noqa
    path("delete-group/", views.DeleteGroupView.as_view(), name="delete_group"),  # noqa
    path('add-perms/', views.AddPermissionsToGroupView.as_view(), name='add_perms'),  # noqa
]


# profile urls
urlpatterns += [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('update-profile/', views.ProfileUpdateView.as_view(), name='update_profile'),
    path('reset-password/', views.PasswordResetView.as_view(), name='reset_password'),
]
