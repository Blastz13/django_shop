from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import View
from datetime import datetime

from .models import Feed
from .models import OurBrand

from .forms import CommentForm


class HomePage(View):
    def get(self, request):
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

        our_brands = OurBrand.objects.all()

        return render(request, 'core/index.html', context={"feeds": slider_feeds,
                                                           "small_feeds": small_feeds,
                                                           "our_brands": our_brands,
                                                           })


class FeedDetail(View):
    def get(self, request, slug):
        feed = get_object_or_404(Feed, slug__iexact=slug)
        #
        # print(feed.get_next_by_date_publicate())
        # print(feed.get_previous_by_date_publicate())
        comment_form = CommentForm()
        return render(request, 'core/blog-post-img.html', context={'feed': feed,
                                                                   'comment_form': comment_form,
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
