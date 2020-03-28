from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from core.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='HomePage'),
    path('blog/', FeedList.as_view(), name='FeedList'),
    path('blog/<str:category>/<str:slug>/', FeedDetail.as_view(), name='FeedDetail'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
