from django import template

from core.models import OurBrand

register = template.Library()


@register.inclusion_tag('shop/inclusion_html/widget-our-brands.html')
def our_brands():
    return {'our_brands': OurBrand.objects.all()}


@register.inclusion_tag('shop/inclusion_html/widget-breadcrumb-area.html')
def breadcrumb_area(obj_product=None):
    return {'obj_title_product': obj_product.title,
            'obj_category_product': obj_product.category.get_ancestors(include_self=True)}


@register.inclusion_tag('shop/inclusion_html/widget-breadcrumb-area-shop.html')
def breadcrumb_area_shop(obj_selected_category=None):
    if not obj_selected_category:
        return {}
    return {'tree_categories': obj_selected_category.get_ancestors(include_self=True)}

