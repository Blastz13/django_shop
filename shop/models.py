from django.db import models
from django.shortcuts import reverse
from django.contrib.postgres.fields import JSONField
from mptt.models import MPTTModel, TreeForeignKey

from PIL import Image

from .utils import path_upload


class Product(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название товара')
    description = models.TextField(max_length=10000, verbose_name='Описание товара')
    preview_image = models.ImageField(upload_to=path_upload('Shop/Product'), default='default_img/product.jpg',
                                      blank=True, null=True,
                                      verbose_name='Изображения для предпросмотра')
    slug = models.SlugField(unique=True, verbose_name='Ссылка на товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена по скидке')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='product', verbose_name='Категория')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество товара')
    is_available = models.BooleanField(verbose_name='Товар в наличии')
    property = JSONField(blank=True, null=True, verbose_name='Свойства товара')
    date_publicate = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления товара')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок показа товара')
    is_publish = models.BooleanField(default=False, verbose_name='Опубликовать')
    count_views = models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров')
    count_buys = models.PositiveBigIntegerField(default=0, verbose_name='Количество покупок')

    def get_product_image(self):
        return self.image.all()

    def get_product_url(self):
        return self.category.get_category_url() + '/' + self.slug

    def get_absolute_url(self):
        path = self.get_product_url()
        return reverse('CategoryProduct', kwargs={
            'slug': path
        })

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        image = Image.open(self.preview_image.path)
        if image.width < 270 or image.height < 340:
            fill_color = '#A36FFF'
            back = Image.new('RGB', (270, 340), fill_color)
            w = int((270 - image.width) / 2)
            h = int((340 - image.height) / 2)
            back.paste(image, (w, h))
            back.save(self.preview_image.path, quality=70, optimize=True)
        else:
            image.save(self.preview_image.path, quality=70, optimize=True)
        return image

    class Meta:
        ordering = ['order', '-date_publicate']
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(models.Model):
    image = models.ImageField(upload_to=path_upload('Shop/Product/Image'), verbose_name='Изображения товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image', verbose_name='Товар')

    def save(self, *args, **kwargs):
        super(ProductImage, self).save(*args, **kwargs)
        image = Image.open(self.image.path)
        image.save(self.image.path, quality=70, optimize=True)
        return image

    def __str__(self):
        return f"{self.product.title}"

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'


class Category(MPTTModel):
    title = models.CharField(max_length=64, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=64, unique=True, verbose_name='Ссылка категории')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child',
                            verbose_name='Подкатегория')

    def get_category_url(self):
        return '/'.join([x['slug'] for x in self.get_ancestors(include_self=True).values()])

    def get_absolute_url(self):
        path = self.get_category_url()
        return reverse('CategoryProduct', kwargs={
            'slug': path
        })

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['title']


