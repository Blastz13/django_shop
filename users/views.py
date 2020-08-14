from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.views.generic import View


from .forms import CustomUserCreationForm, LoginForm


class Account(View):
    def get(self, request):
        form_registration = CustomUserCreationForm()
        form_login = LoginForm()
        return render(request, 'users/my-account.html', context={'form_registration': form_registration,
                                                                 'form_login': form_login})

    def post(self, request):
        form_registration = CustomUserCreationForm()
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            cd = form_login.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if (user is not None) and user.is_active:
                login(request, user)
                return redirect('HomePage')
            else:
                return render(request, 'users/my-account.html', context={'form_registration': form_registration,
                                                                         'form_login': form_login})
        return render(request, 'users/my-account.html', context={'form_registration': form_registration,
                                                                 'form_login': form_login})


@require_POST
def sign_up(request):
    form_registration = CustomUserCreationForm(request.POST)
    form_login = LoginForm()

    if form_registration.is_valid():
        email = form_registration.cleaned_data.get('email')
        password = form_registration.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)
        form_registration.save()
        return redirect('HomePage')
    else:
        return render(request, 'users/my-account.html', {'form_registration': form_registration,
                                                         'form_login': form_login})
