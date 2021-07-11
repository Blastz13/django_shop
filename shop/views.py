from django.db.models import Min, Max
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import View

from .cart import Cart
from .forms import CartAddProductForm, OrderUnregisteredUserForm, OrderUserForm, ProductCommentForm
from .mixins import ObjectSortPaginate
from .models import Product, Category, ProductComment


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

        sort_by = sort_by_key.setdefault(request.GET.get('sort_by', ''), 'order')

        all_products = Product.objects.filter(is_publish=True,
                                              price__gte=price_range_min_filter,
                                              price__lte=price_range_max_filter).order_by(sort_by)
        context = self.get_pagination(all_products, 12)
        context['all_category'] = Category.objects.all()
        context['price_range'] = Product.objects.filter(is_publish=True).aggregate(Min('price'), Max('price'))
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
            product.count_views += 1
            product.save()

            if product.get_product_url() != user_slug:
                return HttpResponse('404 - 2')
            form = CartAddProductForm(request.POST or None, extra={'slug': category_slug[-1],
                                                                   'cart': Cart(request)})
            form_product_comment = ProductCommentForm()
            return render(request, 'shop/product-virtual.html', context={'product': product,
                                                                         'form': form,
                                                                         'form_product_comment': form_product_comment})

        else:
            sort_by = sort_by_key.setdefault(request.GET.get('sort_by', ''), 'order')
            products_by_category = Product.objects.filter(category__in=category.get_descendants(include_self=True),
                                                          is_publish=True,
                                                          price__gte=price_range_min_filter,
                                                          price__lte=price_range_max_filter).order_by(sort_by)
            context = self.get_pagination(products_by_category)
            context['all_category'] = Category.objects.all()
            context['price_range'] = Product.objects.filter(category__in=category.get_descendants(include_self=True),
                                                            is_publish=True).aggregate(Min('price'), Max('price'))
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


class AddProductComment(View):
    def post(self, request, slug):
        form = ProductCommentForm(request.POST)
        product = Product.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.save()
        return redirect(product.get_absolute_url())


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


sort_by_key = {
    'default': '-order',
    'views': '-count_views',
    'newness': '-date_publicate',
    'price' : 'price',
    '-price': '-price'
}
