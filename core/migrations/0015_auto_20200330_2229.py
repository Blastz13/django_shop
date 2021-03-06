# Generated by Django 3.0.4 on 2020-03-30 19:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20200329_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('subject', models.CharField(max_length=64, verbose_name='Тема')),
                ('message', models.TextField(max_length=1000, verbose_name='Сообщение')),
                ('date_send', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
            ],
            options={
                'verbose_name': 'Сообщения контактной формы',
                'verbose_name_plural': 'Сообщения контактной формы',
                'ordering': ['-date_send'],
            },
        ),
        migrations.AlterField(
            model_name='feed',
            name='date_published_from',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 3, 30, 22, 29, 1, 686111), null=True, verbose_name='Опубликовать c'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='date_published_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 4, 6, 22, 29, 1, 686111), null=True, verbose_name='Опубликовать до'),
        ),
    ]
