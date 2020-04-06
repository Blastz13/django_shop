from django.db import models
from django.contrib.postgres.fields import JSONField


class Product(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название товара')
    description = models.TextField(max_length=10000, verbose_name='Описание товара')
    slug = models.SlugField(unique=True, verbose_name='Ссылка на товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    discount_price = models.PositiveIntegerField(blank=True, verbose_name='Цена по скидке')
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
