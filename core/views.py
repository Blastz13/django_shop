from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import View
from django.core.paginator import Paginator

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
    def get(self, request, category, slug):
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

        last_three_feeds = Feed.objects.filter(is_publish=True,
                                               is_blog=True,
                                               date_published_from__lte=datetime.now(tz=timezone.utc))[0:3]
        # TODO: add fitering
        return render(request, 'core/blog-post-img.html', context={'feed': feed,
                                                                   'comment_form': comment_form,
                                                                   'next_feed': next_obj_feed,
                                                                   'previous_feed': previuos_obj_feed,
                                                                   })

    def post(self, request, category, slug):
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

        last_three_feeds = Feed.objects.filter(is_publish=True,
                                               is_blog=True,
                                               date_published_from__lte=datetime.now(tz=timezone.utc))[0:3]
        paginator = Paginator(feeds_all, 4)
        number_page = request.GET.get('page', 1)
        feed_page = paginator.get_page(number_page)
        is_has_other_page = feed_page.has_other_pages()

        if feed_page.has_previous():
            prev_page = f"?page={feed_page.previous_page_number()}"
        else:
            prev_page = ""

        if feed_page.has_next():
            next_page = f"?page={feed_page.next_page_number()}"
        else:
            next_page = ""

        return render(request, 'core/blog.html', context={'feeds_all': feed_page,
                                                          'is_has_other_page': is_has_other_page,
                                                          'next_page': next_page,
                                                          'prev_page': prev_page,
                                                          })
