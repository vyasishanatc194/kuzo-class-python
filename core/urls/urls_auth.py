from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include

from . import views

app_name = "auth"

urlpatterns = [
    # User
    path("users/", views.UserListView.as_view(), name="user-detail"),

    path("users/", views.UserListView.as_view(), name="user-list"),
    path("users/create/", views.UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/update/", views.UserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
    path(
        "users/<int:pk>/password/",
        views.UserPasswordView.as_view(),
        name="user-password",
    ),
    path("ajax-users", views.UserAjaxPagination.as_view(), name="user-list-ajax"),
]

urlpatterns += [
    # Group
    path("groups/", views.GroupListView.as_view(), name="group-list"),
    path("groups/create/", views.GroupCreateView.as_view(), name="group-create"),
    path(
        "groups/<int:pk>/update/", views.GroupUpdateView.as_view(), name="group-update"
    ),
    path(
        "groups/<int:pk>/delete/", views.GroupDeleteView.as_view(), name="group-delete"
    ),
     
]

 
urlpatterns += [

  
    # Login / Logout
    path("login/", auth_views.LoginView.as_view(), name="auth_login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        {'next_page': 'core:auth_login'},  # redirect user
        name="auth_logout",
    ),
    # Password Change
    path(
        "password/change/",
        auth_views.PasswordChangeView.as_view(),
        name="auth_password_change",
    ),
    path(
        "password/change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    # Password reset
    path(
        "password/reset/",
        auth_views.PasswordResetView.as_view(),
        name="auth_password_reset",
    ),
    re_path(
        r"^auth_password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
        auth_views.PasswordResetConfirmView.as_view(),
        name="auth_password_reset_confirm",
    ),
    path(
        "auth_password/reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "auth_password/reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
]

# -----------------------------------------------------------------------------
