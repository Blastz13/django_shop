from django.urls import path
from .views import Account, sign_up, log_out


urlpatterns = [
    path('login/', Account.as_view(), name='Account'),
    path('logout/', log_out, name='Logout'),
    path('signup/', sign_up, name='SignUp'),
]
