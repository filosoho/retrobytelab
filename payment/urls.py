from django.urls import path
from . import views

urlpatterns = [
    path("checkout", views.checkout, name="checkout"),
    path("complete-order", views.complete_order, name="complete-order"),
    path("payment-success", views.payment_success, name="payment-success"),
    path("payment-failed", views.payment_failed, name="payment-failed"),
    path(
        "emails/order-confirmation/<int:order_id>/",
        views.preview_order_confirmation_email,
        name="preview_order_confirmation_email",
    ),
]
