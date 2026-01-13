from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Registration
    path("register/", views.register, name="register"),
    path(
        "email-verification/<str:uidb64>/<str:token>/",
        views.email_verification,
        name="email-verification",
    ),
    path(
        "email-verification-status/<str:status>/",
        views.email_verification_status,
        name="email-verification-status",
    ),
    # Login/Logout
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("delete-account/", views.delete_account, name="delete-account"),
    # Password manager
    path(
        "reset_password",
        auth_views.PasswordResetView.as_view(
            template_name="account/password/password-reset.html"
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password/password-reset-sent.html"
        ),
        name="password_reset_done",
    ),
    # Password reset link
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password/password-reset-form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
    path("manage-shipping/", views.manage_shipping, name="manage-shipping"),
    path("track-orders/", views.track_orders, name="track-orders"),
]
