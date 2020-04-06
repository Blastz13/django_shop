from django import template

from core.models import OurBrand

register = template.Library()


@register.inclusion_tag('shop/inclusion_html/widget-our-brands.html')
def our_brands():
    return {'our_brands': OurBrand.objects.all()}
