from django.shortcuts import render, redirect, HttpResponse
from .models import Herd
from .models import Offspring
from ..users.models import User
from django.contrib import messages

def index(request):
    if not request.session['loggedin']== True:
        return redirect('muleshoe:admin')
    else:
        context = {
            'loggedin': User.objects.get(id = request.session['user']),
            'animals': Herd.objects.all().order_by('species', 'tag'),
        }
        return render(request, 'herd/dashboard.html', context)

def add(request):
    if not request.session['loggedin']== True:
        return redirect('muleshoe:admin')
    else:
        return render(request, 'herd/add.html')

def view(request, id):
    if not request.session['loggedin']== True:
        return redirect('muleshoe:admin')
    else:
        context = {
            'animals': Herd.objects.get(id = id),
            'offspring': Offspring.objects.filter(animal_id = id).order_by('-date_of_birth'),
            'dadOffspring': Offspring.objects.filter(sire_id = id).order_by('-date_of_birth'),
            'loggedin': User.objects.get(id = request.session['user']),
        }
        return render(request, 'herd/view.html', context)

def create(request):
    if request.method == 'POST':
        errors = Herd.objects.add_validator(request.POST)
        if not errors:
            Herd.objects.add(request.POST)
            return redirect('herd:dashboard')
        elif len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)
                return redirect('herd:add')

def addOff(request):
    if request.method == 'POST':
        errors = Offspring.objects.offValidator(request.POST)
        if not errors:
            Offspring.objects.addOff(request.POST)
            return redirect("/view/"+request.POST['id'])
        elif len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags= tag)
                return redirect("/view/"+request.POST['id'])

def delete(request, id):
    Herd.objects.delete(request.POST, id)
    return redirect('herd:dashboard')