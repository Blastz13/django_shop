from django.urls import path
from .views import ProductList
from .views import CategoryProduct, cart_add

urlpatterns = [
    path('', ProductList.as_view(), name='ProductList'),
    path('category/<path:slug>/', CategoryProduct.as_view(), name='CategoryProduct'),
    path('cart/add/<str:slug>/', cart_add, name='CartAdd')
]
