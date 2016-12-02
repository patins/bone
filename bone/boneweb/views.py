from django.shortcuts import render
from .models import Resident, REXEvent, Quote

from django.http import Http404

from django.utils import timezone

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

def home(request):
    rex_events = REXEvent.objects.filter(end__gt=timezone.now(), visible=True).order_by('start')
    return render(request, 'boneweb/home.html', {'rex_events': rex_events})

def about(request):
    rex_events = REXEvent.objects.filter(end__gt=timezone.now(), visible=True).order_by('start')
    return render(request, 'boneweb/about.html', {'rex_events': rex_events})

def residents(request):
    visible_residents = Resident.objects.filter(visible=True, alumni=False)
    ordered_residents = visible_residents.order_by('year', 'name')
    all_years = visible_residents.values_list('year', flat=True).distinct().order_by('year')
    visible_alums = Resident.objects.filter(visible=True, alumni=True)
    ordered_alums = visible_alums.order_by('year', 'name')
    return render(request, 'boneweb/residents.html', {'residents': ordered_residents, 'alumni': ordered_alums, 'all_years': all_years})

def residents_by_year(request, year):
    all_years = Resident.objects.filter(visible=True, alumni=False).values_list('year', flat=True).distinct().order_by('year')
    visible_residents = Resident.objects.filter(visible=True, year=year, alumni=False).order_by('name')
    if visible_residents.count() == 0:
        raise Http404()
    visible_alums = Resident.objects.filter(visible=True, alumni=True)
    return render(request, 'boneweb/residents.html', {'residents': visible_residents, 'year': year, 'all_years': all_years, 'alumni': visible_alums})

def alumni(request):
    visible_residents = Resident.objects.filter(visible=True, alumni=False)
    all_years = visible_residents.values_list('year', flat=True).distinct().order_by('year')
    visible_alums = Resident.objects.filter(visible=True, alumni=True)
    ordered_alums = visible_alums.order_by('year', 'name')
    return render(request, 'boneweb/residents.html', {'residents': ordered_alums, 'alumni': ordered_alums, 'all_years': all_years})

def quotes(request):
    viewable_quotes = Quote.objects.filter(visible=True).order_by('-submitted_at') # last submitted at top
    if not request.user.is_authenticated():
        viewable_quotes = viewable_quotes.filter(public=True)
    return render(request, 'boneweb/quotes.html', {'quotes': viewable_quotes})

"""
from django.conf import settings
import os
from django.views.static import serve

def resident_image(request, year, kerberos):
    the_resident = Resident.objects.filter(year=year, kerberos=kerberos).first()
    if settings.DEBUG:
        return serve(request, the_resident.picture.name, settings.MEDIA_ROOT)
    else:
        response = HttpResponse()
        if the_resident.picture:
            response[settings.SENDFILE_HEADER] = \
                the_resident.picture.path
        else:
            raise Http404()
        return response
"""
