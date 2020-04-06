from django.shortcuts import render
from django.views.generic import View
from .models import Product

# TODO: 'create OurBrand inclusion tag in core and shop'

class ProductList(View):
    def get(self, request):
        return render(request, 'shop/shop.html', context={'all_products': Product.objects.all()})