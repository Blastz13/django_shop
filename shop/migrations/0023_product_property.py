# Generated by Django 3.2.5 on 2021-08-04 07:03

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_auto_20210804_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='property',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Свойства товара'),
        ),
    ]
