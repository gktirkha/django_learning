from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpRequest


def login_view(request: HttpRequest):
    form = None
    context = {}
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(user=user, request=request)
            return redirect("/")

    else:
        form = AuthenticationForm(request=request)

    context['form'] = form

    return render(request=request, template_name='account/login.html', context=context)


def logout_view(request: HttpRequest):
    if (request.method == 'POST'):
        logout(request=request)
        return redirect('/login/')

    return render(request=request, template_name='account/logout.html')


def signup_view(request: HttpRequest):
    context = {}
    signup_form = UserCreationForm(request.POST or None)
    if signup_form.is_valid():
        signup_form.save()
        return redirect("/login")

    context['form'] = signup_form
    return render(request=request, context=context, template_name='account/signup.html')
