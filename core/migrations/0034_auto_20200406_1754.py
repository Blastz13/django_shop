# Generated by Django 3.0.4 on 2020-04-06 14:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20200405_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='date_published_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 4, 13, 14, 54, 1, 391940, tzinfo=utc), null=True, verbose_name='Опубликовать до'),
        ),
    ]
