from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.views.decorators.http import require_POST
from django.views.generic import View

from .cart import Cart

from .mixins import ObjectSortPaginate

from .forms import CartAddProductForm

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

        except:
            product = get_object_or_404(Product, slug=category_slug[-1], is_publish=True)
    
            if product.get_product_url() != user_slug:
                return HttpResponse('404 - 2')
            form = CartAddProductForm(request.POST or None, extra={'slug': category_slug[-1]})
            return render(request, 'shop/product-virtual.html', context={'product': product,
                                                                         'form': form})

        else:
            products_by_category = Product.objects.filter(category__in=category.get_descendants(include_self=True), is_publish=True)
            context = self.get_pagination(products_by_category)
            context['obj_selected_category'] = category
            return render(request, 'shop/shop.html', context=context)


@require_POST
def cart_add(request, slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=slug)
    form = CartAddProductForm(request.POST, extra={'slug': slug})
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd.pop('quantity')
        cart.add(product=product,
                 quantity=quantity,
                 property=cd)
    return HttpResponseRedirect(reverse('CategoryProduct', kwargs={'slug': product.get_product_url()}))
