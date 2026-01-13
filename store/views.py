from django.shortcuts import render
from .models import Category, Product
from django.shortcuts import get_object_or_404


def store(request, category_slug=None):
    category = None
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # HTMX request → return ONLY the grid
    if request.headers.get("HX-Request"):
        return render(
            request,
            "store/components/products_grid.html",
            {
                "products": products,
                "title": category.name if category else "All products",
                "category": category,
                "all_categories": Category.objects.all(),
            },
        )

    # Normal page load
    return render(
        request,
        "store/store.html",
        {
            "products": products,
            "category": category,
        },
    )


def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    context = {
        "product": product,
    }

    return render(request, "store/product-info.html", context)


def categories(request):
    all_categories = Category.objects.all()
    return {"all_categories": all_categories}


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    context = {
        "category": category,
        "products": products,
    }

    return render(request, "store/category-list.html", context)
