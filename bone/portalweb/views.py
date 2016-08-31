from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from boneweb.models import Resident, Quote
from .forms import ResidentForm, QuoteForm

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
