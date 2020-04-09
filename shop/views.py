from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import Product
from .models import Category


class ProductList(View):
    def get(self, request):
        return render(request, 'shop/shop.html', context={'all_products': Product.objects.filter(is_publish=True)})


class CategoryProduct(View):
    def get(self, request, slug):
        user_slug = slug
        category_slug = slug.split('/')
        parent = None
        root = Category.objects.all()

        try:
            for slug in category_slug[:-1]:
                parent = root.get(parent=parent, slug=slug)
        except:
            return HttpResponse('404 - 1')

        try:
            instance = get_object_or_404(Category, parent=parent, slug=category_slug[-1])
        except:
            obj = get_object_or_404(Product, slug=category_slug[-1], is_publish=True)
    
            if obj.get_product_url() != user_slug:
                return HttpResponse('404 - 2')
            # a.get_ancestors(include_self=True)
            return render(request, 'shop/product-virtual.html', context={'product': obj})

        else:
            return HttpResponse(instance.title)
