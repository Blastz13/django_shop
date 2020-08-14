from django.urls import path
from .views import Account, sign_up


urlpatterns = [
    path('login/', Account.as_view(), name='Account'),
    path('signup/', sign_up, name='SignUp'),
]
