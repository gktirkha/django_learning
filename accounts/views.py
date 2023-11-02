from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpRequest


def login_view(request: HttpRequest):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request=request, username=username, password=password,)

        if user is None:
            return render(request=request, template_name='account/login.html', context={"error": "Invalid Username Or Password"})

        login(user=user,request=request)
        return redirect("/admin")

    return render(request=request, template_name='account/login.html', context={})
