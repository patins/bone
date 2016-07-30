from django.shortcuts import render
from .models import Resident

from django.http import Http404

def home(request):
    return render(request, 'boneweb/home.html')

def about(request):
    return render(request, 'boneweb/about.html')

def residents(request):
    visible_residents = Resident.objects.filter(visible=True)
    ordered_residents = visible_residents.order_by('year', 'name')
    all_years = visible_residents.values_list('year', flat=True).distinct().order_by('year')
    return render(request, 'boneweb/residents.html', {'residents': ordered_residents, 'all_years': all_years})

def residents_by_year(request, year):
    all_years = Resident.objects.filter(visible=True).values_list('year', flat=True).distinct().order_by('year')
    visible_residents = Resident.objects.filter(visible=True, year=year).order_by('name')
    if visible_residents.count() == 0:
        raise Http404()
    return render(request, 'boneweb/residents.html', {'residents': visible_residents, 'year': year, 'all_years': all_years})

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
