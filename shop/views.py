from django.db.models import Min, Max
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import View

from .cart import Cart
from .forms import CartAddProductForm, OrderUnregisteredUserForm, OrderUserForm
from .mixins import ObjectSortPaginate
from .models import Product, Category


class ProductList(ObjectSortPaginate, View):
    def get(self, request):
        try:
            price_range_min_filter = float(request.GET['min-value'])
        except:
            price_range_min_filter = 0
        try:
            price_range_max_filter = float(request.GET['max-value'])
        except:
            price_range_max_filter = 10*100

        all_products = Product.objects.filter(is_publish=True,
                                              price__gte=price_range_min_filter,
                                              price__lte=price_range_max_filter)
        context = self.get_pagination(all_products, 12)
        context['all_category'] = Category.objects.all()
        context['price_range'] = all_products.aggregate(Min('price'), Max('price'))
        context['price_range']['price__min'] = str(context['price_range']['price__min'])
        context['price_range']['price__max'] = str(context['price_range']['price__max'])
        return render(request, 'shop/shop.html', context=context)



class CategoryProduct(ObjectSortPaginate, View):
    def get(self, request, slug):
        try:
            price_range_min_filter = float(request.GET['min-value'])
        except:
            price_range_min_filter = 0
        try:
            price_range_max_filter = float(request.GET['max-value'])
        except:
            price_range_max_filter = 10*100
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
            form = CartAddProductForm(request.POST or None, extra={'slug': category_slug[-1],
                                                                   'cart': Cart(request)})
            return render(request, 'shop/product-virtual.html', context={'product': product,
                                                                         'form': form})

        else:
            products_by_category = Product.objects.filter(category__in=category.get_descendants(include_self=True),
                                                          is_publish=True,
                                                          price__gte=price_range_min_filter,
                                                          price__lte=price_range_max_filter)
            context = self.get_pagination(products_by_category)
            context['all_category'] = Category.objects.all()
            context['price_range'] = products_by_category.aggregate(Min('price'), Max('price'))
            context['price_range']['price__min'] = str(context['price_range']['price__min'])
            context['price_range']['price__max'] = str(context['price_range']['price__max'])
            context['obj_selected_category'] = category
            return render(request, 'shop/shop.html', context=context)

    def post(self, request, slug):
        cart = Cart(request)

        product = get_object_or_404(Product, slug=slug)
        form = CartAddProductForm(request.POST, extra={'slug': slug,
                                                      'cart': Cart(request)})
        success_form = CartAddProductForm(extra={'slug': slug,
                                                 'cart': Cart(request)})
        if form.is_valid():
            cd = form.cleaned_data
            price = cd.pop('total_price')
            quantity = cd.pop('quantity')
            cart.add(product=product,
                     price=price,
                     quantity=quantity,
                     property=cd)
        else:
            return render(request, 'shop/product-virtual.html', context={'product': product, 'form': form})
        return render(request, 'shop/product-virtual.html', context={'product': product, 'form': success_form})


class CartProduct(View):
    def get(self, requset):
        cart = Cart(requset)
        return render(requset, 'shop/cart.html', context={'cart': cart})


class Checkout(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = OrderUserForm()
        else:
            form = OrderUnregisteredUserForm()
        cart = Cart(request)
        return render(request, 'shop/checkout.html', context={'cart': cart,
                                                              'form': form})


@require_POST
def cart_del(request, slug):
    cart = Cart(request)
    cart.remove(slug)
    return redirect('CartProduct')
