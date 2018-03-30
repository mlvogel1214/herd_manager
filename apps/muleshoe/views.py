from django.shortcuts import render, redirect

def admin(request):
    return render(request, 'users/index.html')
def about(request):
    return render(request, 'muleshoe/about.html')
def home(request):
    return render(request, 'muleshoe/home.html')