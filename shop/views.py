from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .mixins import ObjectSortPaginate

from .models import Product
from .models import Category


class ProductList(ObjectSortPaginate, View):
    def get(self, request):
        all_products = Product.objects.filter(is_publish=True)
        context = self.get_pagination(all_products, 12)
        return render(request, 'shop/shop.html', context=context)


class CategoryProduct(ObjectSortPaginate, View):
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
            category = get_object_or_404(Category, parent=parent, slug=category_slug[-1])
            print(category.get_descendants(include_self=True))
        except:
            product = get_object_or_404(Product, slug=category_slug[-1], is_publish=True)
    
            if product.get_product_url() != user_slug:
                return HttpResponse('404 - 2')
            # a.get_ancestors(include_self=True)
            return render(request, 'shop/product-virtual.html', context={'product': product})

        else:
            products_by_category = Product.objects.filter(category__in=category.get_descendants(include_self=True), is_publish=True)
            return render(request, 'shop/shop.html', context=self.get_pagination(products_by_category))
