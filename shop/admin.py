from django.contrib import admin
from .models import Product

from django.contrib.postgres.fields import JSONField
from django_json_widget.widgets import JSONEditorWidget


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_price', 'slug']
    list_display_links = ['title', 'price', 'discount_price', 'slug']
    search_fields = ('title', 'description', 'price', 'discount_price')
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
