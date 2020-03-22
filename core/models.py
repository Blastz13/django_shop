from django.db import models


class Feed(models.Model):
    title = models.CharField(max_length=128, blank=True, default='', verbose_name='Заголовок')
    sup_title = models.CharField(max_length=128, blank=True, default='', verbose_name='Подзаголовок')
    body = models.CharField(max_length=512, blank=True, default='', verbose_name='Описание')
    image = models.ImageField(upload_to='', blank=True, null=True, verbose_name='Изображение')
    slug = models.SlugField(max_length=128, unique=True, verbose_name='Ссылка на новость')
    text_button = models.CharField(max_length=64, blank=True, default='', verbose_name='Надпись кнопки')
    url_button = models.SlugField(max_length=512, blank=True, default='', verbose_name='Ссылка кнопки')
    is_slider = models.BooleanField(default=False, verbose_name='Слайдер')
    is_blog = models.BooleanField(default=False, verbose_name='Блог')
    is_publish = models.BooleanField(default=False, verbose_name='Опубликовать')
    date_publicate = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    date_published_from = models.DateTimeField(blank=True, null=True, verbose_name="Опубликовать c")
    date_published_to = models.DateTimeField(blank=True, null=True, verbose_name="Опубликовать до")

    # def get_absolute_url(self):
    #     return reverse('post_detail', kwargs={
    #         'slug': self.slug
    #     })

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['-date_publicate']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
