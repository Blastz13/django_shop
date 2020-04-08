from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Product
from .models import Category

from django.contrib.postgres.fields import JSONField
from django_json_widget.widgets import JSONEditorWidget


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'discount_price', 'slug']
    list_display_links = ['title', 'category', 'price', 'discount_price', 'slug']
    search_fields = ('title', 'category', 'description', 'price', 'discount_price')
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Category)
class AdminCategory(MPTTModelAdmin):
    list_display = ['title', 'slug', 'parent']
    list_display_links = ['title', 'slug', 'parent']
    search_fields = ['title', 'slug', 'parent']

