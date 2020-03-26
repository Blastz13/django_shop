from django.db import models
from django.shortcuts import reverse
from datetime import datetime, timedelta


#TODO: Add tags
#TODO: Add comments
class Feed(models.Model):
    title = models.CharField(max_length=128, blank=True, db_index=True, default='', verbose_name='Заголовок')
    sup_title = models.CharField(max_length=128, blank=True, default='', verbose_name='Подзаголовок')
    description = models.CharField(max_length=512, blank=True, default='', verbose_name='Описание')
    body = models.TextField(max_length=10000, blank=True, default='', verbose_name='Текст статьи')
    image = models.ImageField(upload_to='Feed/%Y/%m/%d/%H', blank=True, null=True, verbose_name='Изображение')
    slug = models.SlugField(max_length=128, unique=True, db_index=True, verbose_name='Ссылка на новость')
    text_button = models.CharField(max_length=64, blank=True, default='', verbose_name='Надпись кнопки')
    url_button = models.SlugField(max_length=512, blank=True, default='', verbose_name='Ссылка кнопки')
    is_slider = models.BooleanField(default=False, verbose_name='Слайдер')
    is_blog = models.BooleanField(default=False, verbose_name='Блог')
    is_publish = models.BooleanField(default=False, verbose_name='Опубликовать')
    date_publicate = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    date_published_from = models.DateTimeField(default=datetime.now(), blank=True, null=True,
                                               verbose_name="Опубликовать c")
    date_published_to = models.DateTimeField(default=datetime.now() + timedelta(days=7), blank=True, null=True,
                                             verbose_name="Опубликовать до")
    tag = models.ManyToManyField('Tag', blank=True, related_name='feeds', verbose_name='Тэг')

    def get_absolute_url(self):
        return reverse('feed_detail', kwargs={
            'slug': self.slug
        })

    def get_comments(self):
        return self.comments.filter(parent__isnull=True)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['-date_publicate']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Ссылка")
    #
    # def get_absolute_url(self):
    #     return reverse('tag_list', kwargs={"slug": self.slug})

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class Comment(models.Model):
    email = models.EmailField(verbose_name='Почта')
    name = models.CharField(max_length=100, verbose_name="Имя")
    text = models.TextField(max_length=5000, verbose_name="Сообщение")
    date_publicate = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    parent = models.ForeignKey("self", verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    feed = models.ForeignKey(Feed, related_name="comments", on_delete=models.CASCADE, verbose_name="Новость")

    def __str__(self):
        return f"{self.name} - {self.feed}"

    class Meta:
        ordering = ["-date_publicate"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class OurBrand(models.Model):
    title = models.CharField(max_length=128, db_index=True, blank=True, verbose_name='Название бренда')
    image = models.ImageField(upload_to='OurBrands/%Y/%m/%d/%H', verbose_name='Логотип')
    order = models.IntegerField(default=0, verbose_name='Порядок')

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['order']
        verbose_name = "Наши бренды"
        verbose_name_plural = "Наши бренды"
