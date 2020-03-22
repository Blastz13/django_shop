from django.shortcuts import render
from django.utils import timezone
from datetime import datetime

from .models import Feed


def index(request):
    slider_feeds = Feed.objects.filter(is_publish=True,
                                       is_slider=True,
                                       date_published_from__lte=datetime.now(tz=timezone.utc),
                                       date_published_to__gte=datetime.now(tz=timezone.utc)
                                       )

    small_feeds = Feed.objects.filter(is_publish=True,
                                      is_blog=True,
                                      date_published_from__lte=datetime.now(tz=timezone.utc),
                                      date_published_to__gte=datetime.now(tz=timezone.utc)
                                      )

    return render(request, 'core/index.html', context={"feeds": slider_feeds,
                                                       "small_feeds": small_feeds,
                                                       })
# Create your views here.
