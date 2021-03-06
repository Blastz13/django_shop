from datetime import datetime, timezone

from django import template

from ..models import Feed
from ..models import Tag
from ..models import OurBrand
from ..models import CategoryFeed

register = template.Library()


# this tag outputs all feeds tags using the template 'template/core/inclusion_html/widget-tags-feeds.html'
@register.inclusion_tag('core/inclusion_html/widget-tags-feeds.html')
def all_tags(slug_selected_tag=None, count=None):
    return {'all_tags': Tag.objects.filter()[:count],
            'slug_selected_tag': slug_selected_tag}


# this tag outputs all feeds using the template 'template/core/inclusion_html/widget-recent-feeds.html'
@register.inclusion_tag('core/inclusion_html/widget-recent-feeds.html')
def recent_feeds(count=3):
    return {'recent_feeds': Feed.objects.filter(is_publish=True,
                                                is_blog=True,
                                                date_published_from__lte=datetime.now(tz=timezone.utc))[0:count]}


# this tag outputs all categories feeds using the template 'template/core/inclusion_html/widget-categories-feeds.html'
@register.inclusion_tag('core/inclusion_html/widget-categories-feeds.html')
def all_categories_feeds(slug_selected_category=None):
    return {'all_categories_feeds': CategoryFeed.objects.all(),
            'slug_selected_category': slug_selected_category}


@register.inclusion_tag('core/inclusion_html/widget-our-brands.html')
def our_brands():
    return {'our_brands': OurBrand.objects.all()}
