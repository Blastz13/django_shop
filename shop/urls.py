from django.urls import path
from .views import ProductList
from .views import CategoryProduct, cart_add, cart_del, CartProduct

urlpatterns = [
    path('', ProductList.as_view(), name='ProductList'),
    path('category/<path:slug>/', CategoryProduct.as_view(), name='CategoryProduct'),
    path('cart/', CartProduct.as_view(), name='CartProduct'),
    path('cart/add/<str:slug>/', cart_add, name='CartAdd'),
    path('cart/del/<str:slug>/', cart_del, name='CartDel')
]
