from django import template

from core.models import OurBrand

register = template.Library()


@register.inclusion_tag('shop/inclusion_html/widget-our-brands.html')
def our_brands():
    return {'our_brands': OurBrand.objects.all()}


@register.inclusion_tag('shop/inclusion_html/widget-breadcrumb-area.html')
def breadcrumb_area(obj_category_product=None):
    print(obj_category_product)
    return {'obj_category_product': obj_category_product.get_ancestors(include_self=True)}
