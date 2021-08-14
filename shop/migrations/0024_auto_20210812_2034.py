# Generated by Django 3.2.5 on 2021-08-12 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_product_property'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='property',
        ),
        migrations.CreateModel(
            name='SpecialCategoryProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Заголовок')),
                ('product', models.ManyToManyField(related_name='special_categories', to='shop.Product', verbose_name='Продукт')),
            ],
        ),
    ]
