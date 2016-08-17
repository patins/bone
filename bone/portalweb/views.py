from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from boneweb.models import Resident, Quote
from .models import Tinder
from django.db.models import Q
from .forms import ResidentForm, TinderForm, QuoteForm

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
def quotes_new(request):
    current_resident = request.user.resident
    quote = Quote(submitter=current_resident)
    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
            form = QuoteForm(instance=quote)
            return redirect('quotes')
        else:
            return render(request, 'portalweb/quotes_new.html', {'form': form })
    else:
        form = QuoteForm()
        return render(request, 'portalweb/quotes_new.html', {'form': form })

@login_required
def quotes_delete(request, quote_id):
    current_resident = request.user.resident
    quote = Quote.objects.get(id=quote_id)
    if (request.method == 'POST' and quote and current_resident and
       (quote.submitter == current_resident or quote.author == current_resident)):
        quote.delete()
        return redirect('quotes')
    return redirect('/')


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

@login_required
@permission_required('tinders.view_all', raise_exception=True)
def tinders(request):
    residents = Resident.objects.filter(Q(alumni=False) | Q(tinder__isnull=False)).order_by('alumni', 'year', 'name')
    return render(request, 'portalweb/tinders.html', { 'residents': residents })
