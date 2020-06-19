from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, price, quantity=1, property=None, update_quantity=False):
        is_added = False
        try:
            product_id = str(int(list(self.cart.keys())[-1])+1)
        except IndexError:
            product_id = 1

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
        # if update_quantity:
        #     self.cart[product_id]['quantity'] = quantity
        # else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product_num):
        product_id = str(product_num)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        # product_ids = []
        for key in self.cart.keys():
            product = Product.objects.get(slug=self.cart[key]['product_slug'])
            self.cart[key]['product'] = product
        # получение объектов product и добавление их в корзину
        # products = Product.objects.filter(slug__in=product_ids)
        # for product in products:
        #     self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return len(self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True