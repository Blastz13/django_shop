from django.db import models
from django.contrib.postgres.fields import JSONField
from mptt.models import MPTTModel, TreeForeignKey


class Product(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название товара')
    description = models.TextField(max_length=10000, verbose_name='Описание товара')
    slug = models.SlugField(unique=True, verbose_name='Ссылка на товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    discount_price = models.PositiveIntegerField(blank=True, verbose_name='Цена по скидке')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='product', verbose_name='Категория')
    is_available = models.BooleanField(verbose_name='Товар в наличии')
    property = JSONField(blank=True, null=True, verbose_name='Свойства товара')
    date_publicate = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления товара')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок показа товара')
    is_publish = models.BooleanField(default=False, verbose_name='Опубликовать')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['order', '-date_publicate']
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Category(MPTTModel):
    title = models.CharField(max_length=64, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=64, unique=True, verbose_name='Ссылка категории')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child', verbose_name='Подкатегория')

    def get_category_url(self):
        return '/'.join([x['slug'] for x in self.get_ancestors(include_self=True).values()])

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['title']