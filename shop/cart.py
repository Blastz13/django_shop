from decimal import Decimal
from django.conf import settings
from shop.models import Product, Order, OrderItem
from django.contrib import messages
import copy


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, price, quantity=1, property=None, update_quantity=False):
        is_added = False
        try:
            product_id = str(int(list(self.cart.keys())[-1])+1)
        except IndexError:
            product_id = '1'

        for key, product_cart in self.cart.items():
            if product_cart['product_slug'] == product.slug and product_cart['property'] == property:
                self.cart[key]['quantity'] += quantity
                is_added = True

        if not is_added:
            self.cart[product_id] = {'product_id': product_id,
                                     'product_slug': product.slug,
                                     'quantity': 0,
                                     'property': property,
                                     'price': price}

            self.cart[product_id]['quantity'] += quantity
        self.save()

    def is_valid(self, request):
        is_valid = True
        for item in self.__class__.__iter__(self):
            product = item['product']

            if not(product.is_available and product.is_publish and product.quantity != 0):
                is_valid = False
                self.remove(item['product_id'])

            if product.quantity < item['quantity']:
                is_valid = False
                self.cart[item['product_id']]['quantity'] = product.quantity

            if product.discount_price:
                if str(product.discount_price) != item['price']:
                    is_valid = False
                    self.cart[item['product_id']]['price'] = str(product.discount_price)
            else:
                if str(product.price) != item['price']:
                    is_valid = False
                    self.cart[item['product_id']]['price'] = str(product.price)

        if is_valid:
            return True
        else:
            self.save()
            messages.error(request, 'Ваша корзина изменилась, не все товары доступны')
            return False

    def create_order(self, request, cd):
        order = Order.objects.create(city=cd['city'],
                                     address=cd['address'],
                                     phone=cd['phone'],
                                     order_notes=cd['order_notes'],
                                     buyer=request.user)
        for order_item in self.__class__.__iter__(self):
            product = order_item['product']
            OrderItem.objects.create(order=order, product=order_item['product'],
                                     price=order_item['price'], quantity=order_item['quantity'])
            product.quantity -= order_item['quantity']
            product.count_buys += 1
            product.save()
        messages.info(request, 'Заказ успешно оформлен')
        self.clear()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product_num):
        product_id = str(product_num)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        self.cart_order = copy.deepcopy(self.cart)
        for key in self.cart_order.keys():
            product = Product.objects.get(slug=self.cart[key]['product_slug'])
            self.cart_order[key]['product'] = product

        for item in self.cart_order.values():
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return len(self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
