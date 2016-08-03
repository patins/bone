from django.shortcuts import render
from .models import Resident

from django.http import Http404

from django.utils import timezone

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

def home(request):
    return render(request, 'boneweb/home.html')

def about(request):
    return render(request, 'boneweb/about.html')

def _current_graduation_year(t=timezone.now()):
    """ Returns the year that graduates should be considering given a datetime"""
    if t.month > 4: # If it's after May it's this year
        return t.year
    else: # If it's before June it's last year
        return t.year - 1

def residents(request):
    grad_year = _current_graduation_year()
    visible_residents = Resident.objects.filter(visible=True, year__gt=grad_year)
    ordered_residents = visible_residents.order_by('year', 'name')
    all_years = visible_residents.values_list('year', flat=True).distinct().order_by('year')
    visible_alums = Resident.objects.filter(visible=True, year__lte=grad_year)
    ordered_alums = visible_alums.order_by('year', 'name')
    return render(request, 'boneweb/residents.html', {'residents': ordered_residents, 'alumni': ordered_alums, 'all_years': all_years})

def residents_by_year(request, year):
    grad_year = _current_graduation_year()
    all_years = Resident.objects.filter(visible=True, year__gt=grad_year).values_list('year', flat=True).distinct().order_by('year')
    visible_residents = Resident.objects.filter(visible=True, year=year).order_by('name')
    if visible_residents.count() == 0:
        raise Http404()
    visible_alums = Resident.objects.filter(visible=True, year__lte=grad_year)
    return render(request, 'boneweb/residents.html', {'residents': visible_residents, 'year': year, 'all_years': all_years, 'alumni': visible_alums})

def alumni(request):
    grad_year = _current_graduation_year()
    visible_residents = Resident.objects.filter(visible=True, year__gt=grad_year)
    all_years = visible_residents.values_list('year', flat=True).distinct().order_by('year')
    visible_alums = Resident.objects.filter(visible=True, year__lte=grad_year)
    ordered_alums = visible_alums.order_by('year', 'name')
    return render(request, 'boneweb/residents.html', {'residents': ordered_alums, 'alumni': ordered_alums, 'all_years': all_years})

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
