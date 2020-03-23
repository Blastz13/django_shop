from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Feed
from .models import OurBrand


@admin.register(Feed)
class AdminFeed(admin.ModelAdmin):
    list_display = ['title', 'slug', 'body', 'get_image', 'is_slider', 'is_blog', 'is_publish', 'date_publicate']
    list_display_links = ['title', 'slug', 'body', 'get_image']

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="640" height="360"')

    get_image.short_description = "Фото"


@admin.register(OurBrand)
class AdminOurBrand(admin.ModelAdmin):
    list_display = ['title', 'get_image', 'order']
    list_display_links = ['title', 'get_image', 'order']

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="320" height="180"')

    get_image.short_description = "Фото"