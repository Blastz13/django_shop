from django.urls import path
from .views import Account, sign_up, log_out, MyAccount
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('login/', Account.as_view(), name='Account'),
    path('logout/', log_out, name='Logout'),
    path('signup/', sign_up, name='SignUp'),
    path('my-account/', login_required(MyAccount.as_view()), name='MyAccount'),
]
