from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

from .models import Product
from .models import ProductComment
from .models import Category
from .models import ProductImage, Order, OrderItem

from django.contrib.postgres.fields import JSONField
from django_json_widget.widgets import JSONEditorWidget


class ProductImageItemInline(admin.StackedInline):
    model = ProductImage
    list_display = ['get_image', 'product']
    list_display_links = ['get_image', 'product']
    search_fields = ['get_image']
    extra = 1

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="640" height="360"')

    get_image.short_description = "Изображение"


class ProductCommentItemInline(admin.TabularInline):
    model = ProductComment
    list_display = ['email', 'name', 'date_publicate', 'product']
    list_display_links = ['email', 'name', 'date_publicate', 'product']
    search_fields = ['email', 'name']
    readonly_fields = ['email', 'name']
    extra = 1


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'discount_price', 'get_image', 'quantity', 'is_available',
                    'is_publish', 'slug']
    list_display_links = ['title', 'category', 'price', 'discount_price', 'slug']
    search_fields = ('title', 'description', 'price', 'discount_price')
    inlines = [ProductImageItemInline, ProductCommentItemInline]
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

    def get_image(self, obj):
        if obj.preview_image:
            return mark_safe(f'<img src={obj.preview_image.url} width="80" height="100"')

    get_image.short_description = "Изображение"


@admin.register(Category)
class AdminCategory(MPTTModelAdmin):
    list_display = ['title', 'slug', 'parent']
    list_display_links = ['title', 'slug', 'parent']
    search_fields = ['title', 'slug']


class AdminOrderItem(admin.StackedInline):
    model = OrderItem
    list_display = ['date_create', 'quantity', 'total_amount']
    list_display_links = ['date_create', 'quantity', 'total_amount']
    extra = 0


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['city', 'address', 'phone', 'order_notes', 'date_create', 'is_paid', 'is_coupon_applied']
    list_display_links = ['city', 'address', 'phone', 'order_notes', 'date_create', 'is_paid', 'is_coupon_applied']
    search_fields = ('city', 'address', 'phone', 'order_notes', 'date_create', 'is_paid', 'is_coupon_applied')
    readonly_fields = ('total_amount', )
    inlines = [AdminOrderItem]
