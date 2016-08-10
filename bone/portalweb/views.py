from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from boneweb.models import Resident
from .models import Tinder
from .forms import ResidentForm, TinderForm

@login_required
def profile(request):
    resident = request.user.resident
    if request.method == 'POST':
        form = ResidentForm(request.POST, request.FILES, instance=resident)
        if form.is_valid():
            form.save()
            form = ResidentForm(instance=resident)
        return render(request, 'portalweb/profile.html', { 'resident': resident, 'form': form })
    else:
        form = ResidentForm(instance=resident)
        return render(request, 'portalweb/profile.html', { 'resident': resident, 'form': form })

@login_required
def tinder(request):
    resident = request.user.resident
    try:
        tinder = resident.tinder
    except Tinder.DoesNotExist:
        tinder = Tinder.objects.create(resident=resident, name=resident.name, picture=resident.picture)
    if request.method == 'POST':
        form = TinderForm(request.POST, request.FILES, instance=tinder)
        if form.is_valid():
            form.save()
            form = TinderForm(instance=tinder)
        return render(request, 'portalweb/tinder.html', { 'resident': resident, 'form': form })
    else:
        form = TinderForm(instance=tinder)
        return render(request, 'portalweb/tinder.html', { 'resident': resident, 'form': form })
