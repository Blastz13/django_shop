# Generated by Django 3.0.4 on 2020-08-12 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20200508_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='preview_image',
            field=models.ImageField(blank=True, default='default_img/product.jpg', null=True, upload_to='wrap', verbose_name='Изображения для предпросмотра'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='wrap', verbose_name='Изображения товара'),
        ),
    ]
