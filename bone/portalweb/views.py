from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from boneweb.models import Resident
from .models import Tinder
from django.db.models import Q
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

TINDER_NOT_COMPLETED_SPECS = Q(tinder__bio="") | Q(tinder__age="") |\
                             Q(tinder__name="") | Q(tinder__picture="") |\
                             Q(tinder__location="")

def tinders_metrics():
    residents_not_alumni = Resident.objects.filter(alumni=False)
    total = residents_not_alumni.count()
    if total == 0:
        return None
    not_started = residents_not_alumni.filter(tinder__isnull=True).count()
    completed = residents_not_alumni.exclude(tinder__isnull=True).exclude(TINDER_NOT_COMPLETED_SPECS).count()
    metrics = {
        'not_started': not_started,
        'not_started_pct': 100.0 * not_started / total,
        'completed': completed,
        'completed_pct': 100.0 * completed / total
    }
    metrics['started'] = total - metrics['not_started'] - metrics['completed']
    metrics['started_pct'] = 100.0 - metrics['not_started_pct'] - metrics['completed_pct']
    return metrics

@login_required
@permission_required('tinders.view_all', raise_exception=True)
def tinders(request):
    only_not_completed = request.GET.get('not_completed') != None
    residents = Resident.objects.order_by('alumni', 'year', 'name')
    if only_not_completed:
        residents = residents.filter(alumni=False).filter(TINDER_NOT_COMPLETED_SPECS | Q(tinder__isnull=True))
    else:
        residents = residents.filter(Q(alumni=False) | Q(tinder__isnull=False))
    residents = residents.prefetch_related('tinder', 'user')
    return render(request, 'portalweb/tinders.html', {
        'residents': residents,
        'only_not_completed': only_not_completed,
        'metrics': tinders_metrics()
    })

@login_required
@permission_required('tinders.view_all', raise_exception=True)
def tinders_print(request):
    only_completed = request.GET.get('only_completed') != None
    residents = Resident.objects.filter(tinder__isnull=False).order_by('alumni', 'year', 'name')
    if only_completed:
        residents = residents.exclude(TINDER_NOT_COMPLETED_SPECS)
    return render(request, 'portalweb/tinders_print.html', { 'residents': residents })
