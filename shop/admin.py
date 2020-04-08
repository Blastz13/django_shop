from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

from .models import Product
from .models import Category
from .models import ProductImage

from django.contrib.postgres.fields import JSONField
from django_json_widget.widgets import JSONEditorWidget


class ProductImageItemInline(admin.StackedInline):
    model = ProductImage
    list_display = ['get_image', 'product']
    list_display_links = ['get_image', 'product']
    search_fields = ['get_image', 'product']
    extra = 1

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="640" height="360"')

    get_image.short_description = "Изображение"

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'discount_price', 'slug']
    list_display_links = ['title', 'category', 'price', 'discount_price', 'slug']
    search_fields = ('title', 'category', 'description', 'price', 'discount_price')
    inlines = [ProductImageItemInline]
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Category)
class AdminCategory(MPTTModelAdmin):
    list_display = ['title', 'slug', 'parent']
    list_display_links = ['title', 'slug', 'parent']
    search_fields = ['title', 'slug', 'parent']


