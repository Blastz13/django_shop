from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import View

from .forms import CommentForm

from .models import Feed
from .models import OurBrand
from .models import Tag


# TODO: edited admin panel
class HomePage(View):
    def get(self, request):
        slider_feeds = Feed.objects.filter(is_publish=True,
                                           is_slider=True,
                                           date_published_from__lte=datetime.now(tz=timezone.utc),
                                           date_published_to__gte=datetime.now(tz=timezone.utc))

        small_feeds = Feed.objects.filter(is_publish=True,
                                          is_blog=True,
                                          date_published_from__lte=datetime.now(tz=timezone.utc),
                                          date_published_to__gte=datetime.now(tz=timezone.utc))

        our_brands = OurBrand.objects.all()

        return render(request, 'core/index.html', context={"feeds": slider_feeds,
                                                           "small_feeds": small_feeds,
                                                           "our_brands": our_brands,
                                                           })


class FeedDetail(View):
    def get(self, request, slug):
        comment_form = CommentForm()
        feed = get_object_or_404(Feed,
                                 slug__iexact=slug,
                                 is_publish=True,
                                 is_blog=True,
                                 date_published_from__lte=datetime.now(tz=timezone.utc))

        try:
            next_obj_feed = feed.get_next_by_date_publicate(is_publish=True,
                                                            is_blog=True,
                                                            date_published_from__lte=datetime.now(tz=timezone.utc))
        except Feed.DoesNotExist:
            next_obj_feed = None

        try:
            previuos_obj_feed = feed.get_previous_by_date_publicate(is_publish=True,
                                                                    is_blog=True,
                                                                    date_published_from__lte=datetime.now(tz=timezone.utc))
        except Feed.DoesNotExist:
            previuos_obj_feed = None

        all_tags_feeds = Tag.objects.all()
        last_three_feeds = Feed.objects.filter(is_publish=True,
                                               is_blog=True,
                                               date_published_from__lte=datetime.now(tz=timezone.utc))[0:3]
        # TODO: add fitering
        return render(request, 'core/blog-post-img.html', context={'feed': feed,
                                                                   'comment_form': comment_form,
                                                                   'next_feed': next_obj_feed,
                                                                   'previous_feed': previuos_obj_feed,
                                                                   'last_three_feeds': last_three_feeds,
                                                                   'all_tags_feeds': all_tags_feeds
                                                                   })

    def post(self, request, slug):
        form = CommentForm(request.POST)
        feed = Feed.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.feed = feed
            form.save()
        return redirect(feed.get_absolute_url())


class FeedList(View):
    def get(self, request):
        feeds_all = Feed.objects.filter(is_publish=True,
                                       is_blog=True,
                                       date_published_from__lte=datetime.now(tz=timezone.utc))
        all_tags_feeds = Tag.objects.all()
        last_three_feeds = Feed.objects.filter(is_publish=True,
                                               is_blog=True,
                                               date_published_from__lte=datetime.now(tz=timezone.utc))[0:3]

        return render(request, 'core/blog.html', context={'feeds_all': feeds_all,
                                                          'all_tags_feeds': all_tags_feeds,
                                                          'last_three_feeds': last_three_feeds
                                                          })
