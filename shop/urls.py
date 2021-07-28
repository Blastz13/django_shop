from django.urls import path
from .views import ProductList
from .views import CategoryProduct, cart_del, CartProduct, Checkout, \
                   AddProductComment, ProductListVertical, CategoryProductVertical, ProductSearch, apply_coupon

urlpatterns = [
    path('', ProductList.as_view(), name='ProductList'),
    path('list/', ProductListVertical.as_view(), name='ProductListVertical'),
    path('category/<path:slug>/', CategoryProduct.as_view(), name='CategoryProduct'),
    path('category-list/<path:slug>/', CategoryProductVertical.as_view(), name='CategoryProductVertical'),
    path('search/', ProductSearch.as_view(), name='ProductSearch'),
    path('cart/', CartProduct.as_view(), name='CartProduct'),
    path('cart/del/<str:slug>/', cart_del, name='CartDel'),
    path('cart/apply-coupon/', apply_coupon, name='ApplyCoupon'),
    path('place-order/', Checkout.as_view(), name='Checkout'),
    path('add-product-comment/<str:slug>/', AddProductComment.as_view(), name='AddProductComment'),
]
