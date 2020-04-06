# Generated by Django 3.0.4 on 2020-04-06 15:55

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20200406_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='shop.Category', verbose_name='Подкатегория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='shop.Category', verbose_name='Категория'),
        ),
    ]
