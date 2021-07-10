# Generated by Django 3.2.5 on 2021-07-10 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20210705_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='count_buys',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Количество покупок'),
        ),
        migrations.AddField(
            model_name='product',
            name='count_views',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров'),
        ),
    ]
