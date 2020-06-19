# Generated by Django 3.0.4 on 2020-04-26 11:23

import ckeditor_uploader.fields
import core.utils
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20200408_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='date_published_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 5, 3, 11, 23, 42, 508774, tzinfo=utc), null=True, verbose_name='Опубликовать до'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='image',
            field=models.ImageField(blank=True, default='default_img/news.jpeg', null=True, upload_to=core.utils.path_upload, verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='title',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', max_length=2048, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='ourbrand',
            name='image',
            field=models.ImageField(upload_to=core.utils.path_upload, verbose_name='Логотип'),
        ),
    ]
