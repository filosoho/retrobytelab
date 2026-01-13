from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='category'),
    path('product/<slug:product_slug>/',
         views.product_info, name='product-info'),
]
