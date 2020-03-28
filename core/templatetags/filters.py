from datetime import datetime, timezone

from django import template

from ..models import Feed
from ..models import Tag
from ..models import OurBrand

register = template.Library()


# this tag outputs all feeds tags using the template 'template/core/inclusion_html/widget-tags-feeds.html'
@register.inclusion_tag('core/inclusion_html/widget-tags-feeds.html')
def all_tags(count=None):
    return {'all_tags': Tag.objects.filter()[:count]}


# this tag outputs all feeds using the template 'template/core/inclusion_html/widget-recent-feeds.html'
@register.inclusion_tag('core/inclusion_html/widget-recent-feeds.html')
def recent_feeds(count=3):
    return {'recent_feeds': Feed.objects.filter(is_publish=True,
                                                is_blog=True,
                                                date_published_from__lte=datetime.now(tz=timezone.utc))[0:count]}


# @register.inclusion_tag('core/inclusion_html/widget-recent-feeds.html')
# def our_brands():
#     return {'our_brands': OurBrand.objects.all()}
