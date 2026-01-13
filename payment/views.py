from django.shortcuts import render
from .models import ShippingAddress, Order, OrderItem
from cart.cart import Cart
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render


def checkout(request):
    cart = Cart(request)
    cart_total = cart.get_total()

    context = {
        "PAYPAL_CLIENT_ID": settings.PAYPAL_CLIENT_ID,
        "cart_total": cart_total,
    }

    # Users with accounts - prefilled form
    if request.user.is_authenticated:
        try:
            # Authenticated with shipping info
            shipping_address = ShippingAddress.objects.get(user=request.user.id)

            context["shipping"] = shipping_address

            return render(request, "payment/checkout.html", context)
        except ShippingAddress.DoesNotExist:
            # Authenticated user without shipping info
            return render(request, "payment/checkout.html", context)

    # Guest users
    return render(request, "payment/checkout.html", context)


def complete_order(request):

    if request.POST.get("action") == "post":

        name = request.POST.get("name")
        email = request.POST.get("email")

        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")

        state = request.POST.get("state")
        zipcode = request.POST.get("zipcode")

        shipping_address = (
            address1 + "\n" + address2 + "\n" + city + "\n" + state + "\n" + zipcode
        )

        cart = Cart(request)

        total_cost = cart.get_total()

        """
         Order variations
        1) Create order -> Account users WITH + WITHOUT shipping information
        2) Create order -> Guest users without an account 
        """
        # 1) Create order -> Account users WITH + WITHOUT shipping information
        if request.user.is_authenticated:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
                user=request.user,
            )

            order_id = order.pk
            print(order_id)
            order_items = []

            for item in cart:

                OrderItem.objects.create(
                    order_id=order_id,
                    product=item["product"],
                    quantity=item["qty"],
                    price=item["price"],
                    user=request.user,
                )

                order_items.append(
                    {
                        "title": item["product"].title,
                        "quantity": item["qty"],
                        "price": item["price"],
                        "image_url": request.build_absolute_uri(
                            item["product"].image.url
                        ),
                    }
                )

            html_content = render_to_string(
                "payment/emails/order_confirmation.html",
                {
                    "name": name,
                    "order_items": order_items,
                    "total": cart.get_total(),
                },
            )

            text_content = strip_tags(html_content)

            email_message = EmailMultiAlternatives(
                subject="Order received",
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )

            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

        #  2) Create order -> Guest users without an account
        else:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
            )

            order_id = order.pk

            order_items = []

            for item in cart:

                OrderItem.objects.create(
                    order_id=order_id,
                    product=item["product"],
                    quantity=item["qty"],
                    price=item["price"],
                )

                order_items.append(
                    {
                        "title": item["product"].title,
                        "quantity": item["qty"],
                        "price": item["price"],
                        "image_url": request.build_absolute_uri(
                            item["product"].image.url
                        ),
                    }
                )

            html_content = render_to_string(
                "payment/emails/order_confirmation.html",
                {
                    "name": name,
                    "order_items": order_items,
                    "total": cart.get_total(),
                },
            )

            text_content = strip_tags(html_content)

            email_message = EmailMultiAlternatives(
                subject="Order received",
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )

            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

        order_success = True

        response = JsonResponse({"success": order_success})

        return response


def payment_success(request):
    # Clear shopping cart
    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]

    context = {
        "icon": "check-circle",
        "icon_class": "text-success",
        "headline": "Payment successful",
        "message": "Thank you for your order. Your payment was processed successfully.",
    }

    return render(request, "payment/payment-status.html", context)


def payment_failed(request):
    context = {
        "icon": "times-circle",
        "icon_class": "text-danger",
        "headline": "Payment failed",
        "message": "Something went wrong while processing your payment. Please try again.",
    }

    return render(request, "payment/payment-status.html", context)


def preview_order_confirmation_email(request, order_id):
    order = Order.objects.get(pk=order_id)

    print("order: ===> ", order)

    order_items = [
        {
            "title": item.product.title,
            "quantity": item.quantity,
            "price": item.price,
            "image_url": (
                request.build_absolute_uri(item.product.image.url)
                if item.product.image
                else None
            ),
        }
        for item in order.orderitem_set.all()
    ]

    return render(
        request,
        "payment/emails/order_confirmation.html",
        {
            "name": order.full_name,
            "order_items": order_items,
            "total": order.amount_paid,
        },
    )
