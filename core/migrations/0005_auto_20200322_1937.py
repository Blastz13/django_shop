# Generated by Django 3.0.4 on 2020-03-22 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200322_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='body',
            field=models.CharField(blank=True, default='', max_length=512, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='sup_title',
            field=models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='Подзаголовок'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='text_button',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='Надпись кнопки'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='title',
            field=models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='url_button',
            field=models.SlugField(blank=True, default='', max_length=512, null=True, verbose_name='Ссылка кнопки'),
        ),
    ]
