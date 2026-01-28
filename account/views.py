from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cart.services import save_session_cart_to_db, load_user_cart_to_session


def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = user_tokenizer_generate.make_token(user)

            verification_url = f"https://{current_site.domain}{reverse('email-verification', kwargs={'uidb64': uid, 'token': token})}"

            subject = "Account verification email."
            message = render_to_string(
                "account/registration/email-verification.html",
                {
                    "user": user,
                    "verification_url": verification_url,
                },
            )

            user.email_user(subject=subject, message=message)

            return redirect("email-verification-status", status="sent")

    context = {"form": form}

    return render(request, "account/registration/register.html", context)


def email_verification(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect("email-verification-status", status="success")
    else:
        return redirect("email-verification-status", status="failed")


def email_verification_status(request, status):
    """Reusable view for all email verification feedback messages."""
    messages_map = {
        "success": {
            "icon": "check",
            "icon_class": "success",
            "headline": "Your account is now verified!",
            "message": "Please proceed to login.",
        },
        "sent": {
            "icon": "envelope",
            "icon_class": "",
            "headline": "A verification link has been sent to your email!",
            "message": "Please check your email.",
        },
        "failed": {
            "icon": "exclamation-triangle",
            "icon_class": "warning",
            "headline": "We couldn't verify your account.",
            "message": "Please contact admin support.",
        },
    }

    context = messages_map.get(status, messages_map["failed"])
    return render(
        request, "account/registration/email-verification-message.html", context
    )


def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                load_user_cart_to_session(request)

                return redirect("dashboard")

    context = {"form": form}

    return render(request, "account/login.html", context=context)


def logout(request):
    if request.user.is_authenticated:
        save_session_cart_to_db(request)

    auth.logout(request)

    messages.success(request, "Logout successful")

    return redirect("store")


@login_required(login_url="login")
def dashboard(request):
    return render(request, "account/dashboard.html")


@login_required(login_url="login")
def profile(request):
    user_form = UpdateUserForm(instance=request.user)

    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            messages.info(request, "Account has been updated")

            return redirect("dashboard")

    context = {"user_form": user_form}

    return render(request, "account/profile.html", context)


@login_required(login_url="login")
def delete_account(request):
    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        user.delete()

        messages.error(request, "Account has been deleted")

        return redirect("store")

    return render(request, "account/delete-account.html")


# Shipping
@login_required(login_url="login")
def manage_shipping(request):
    try:
        # Account user with shipment information
        shipping = ShippingAddress.objects.get(user=request.user.id)
    except ShippingAddress.DoesNotExist:
        shipping = None

    form = ShippingForm(instance=shipping)

    if request.method == "POST":
        form = ShippingForm(request.POST, instance=shipping)

    if form.is_valid():
        shipping_user = form.save(commit=False)
        shipping_user.user = request.user
        shipping_user.save()

        return redirect("dashboard")

    context = {"form": form}

    return render(request, "account/manage-shipping.html", context)


@login_required(login_url="login")
def track_orders(request):
    try:
        orders = (
            Order.objects.filter(user=request.user)
            .prefetch_related("items__product")
            .order_by("-id")
        )

        context = {"orders": orders}

        return render(request, "account/track-orders.html", context)

    except OrderItem.DoesNotExist:

        return render(request, "account/track-orders.html")
