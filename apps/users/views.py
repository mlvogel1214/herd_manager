from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages


def index(request):
    request.session['loggedin'] = False
    return render(request, 'users/index.html')
def create_new(request):
    request.session['loggedin']= True
    return render(request, 'users/register.html')

def register(request):
    errors = User.objects.register_validate(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect('users:create_new')
    else:
        user = User.objects.register(request.POST)
        request.session['user'] = user.id
        request.session['first_name']= user.first_name
        request.session['loggedin'] = True
        return redirect('herd:dashboard')

def login(request):
    errors = User.objects.login_validate(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect('users:index')
    else:
        user = User.objects.login(request.POST)
        request.session['user'] = user.id
        request.session['first_name']= user.first_name
        request.session['loggedin'] = True
        return redirect('herd:dashboard')

def logout(request):
    request.session.clear()
    return redirect('users:index')