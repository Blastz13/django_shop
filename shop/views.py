from django.shortcuts import render
from django.views.generic import View
from .models import Product


class ProductList(View):
    def get(self, request):
        return render(request, 'shop/shop.html', context={'all_products': Product.objects.all()})