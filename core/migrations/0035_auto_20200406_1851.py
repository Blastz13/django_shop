# Generated by Django 3.0.4 on 2020-04-06 15:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20200406_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='date_published_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 4, 13, 15, 51, 56, 883407, tzinfo=utc), null=True, verbose_name='Опубликовать до'),
        ),
    ]
