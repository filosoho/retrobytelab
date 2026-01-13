from cart.models import Cart as CartModel, CartItem


def load_user_cart_to_session(request):
    cart_model, _ = CartModel.objects.get_or_create(user=request.user)

    session_cart = {}
    for item in cart_model.items.all():
        session_cart[str(item.product.id)] = {
            'qty': item.qty,
            'price': str(item.product.price),
        }

    request.session['session_key'] = session_cart
    request.session.modified = True


def save_session_cart_to_db(request):
    cart_model, _ = CartModel.objects.get_or_create(user=request.user)

    # Clear existing DB cart items
    CartItem.objects.filter(cart=cart_model).delete()

    session_cart = request.session.get('session_key', {})

    for product_id, data in session_cart.items():
        CartItem.objects.create(
            cart=cart_model,
            product_id=product_id,
            qty=data['qty'],
        )
