from django.shortcuts import render, redirect
from .models import Resident
from .forms import ResidentForm

from django.conf import settings
from django.contrib import auth
from django.utils.crypto import get_random_string
from django.utils.http import urlencode
import hmac
import hashlib

from django.http import Http404, HttpResponse

def home(request):
    return render(request, 'boneweb/home.html')

def about(request):
    return render(request, 'boneweb/about.html')

def residents(request):
    visible_residents = Resident.objects.filter(visible=True)
    ordered_residents = visible_residents.order_by('year', 'name')
    all_years = visible_residents.values_list('year', flat=True).distinct()
    return render(request, 'boneweb/residents.html', {'residents': ordered_residents, 'all_years': all_years})

def residents_by_year(request, year):
    all_years = Resident.objects.filter(visible=True).values_list('year', flat=True).distinct()
    visible_residents = Resident.objects.filter(visible=True, year=year).order_by('name')
    if visible_residents.count() == 0:
        raise Http404()
    return render(request, 'boneweb/residents.html', {'residents': visible_residents, 'year': year, 'all_years': all_years})

def profile(request):
    if not request.user.is_authenticated():
        return redirect('home')
    resident = Resident.objects.get(user=request.user)
    if request.method == 'POST':
        form = ResidentForm(request.POST, request.FILES, instance=resident)
        if form.is_valid():
            form.save()
            form = ResidentForm(instance=resident)
        return render(request, 'boneweb/profile.html', { 'resident': resident, 'form': form })
    else:
        form = ResidentForm(instance=resident)
        return render(request, 'boneweb/profile.html', { 'resident': resident, 'form': form })

def verify_token(token, email, signature):
    message = "{0}:{1}".format(token, email).encode('utf-8')
    h = hmac.new(settings.SCRIPTS_AUTH_KEY, message, hashlib.sha256)
    print(h.hexdigest(), signature)
    return hmac.compare_digest(h.hexdigest(), signature)

def login(request):
    if request.user.is_authenticated():
        return redirect('home')
    else:
        if request.GET.get('email') and request.GET.get('signature') and request.session.get('token'):
            token = request.session['token']
            del request.session['token']
            email = request.GET['email']
            signature = request.GET['signature']
            if verify_token(token, email, signature):
                kerberos = email.lower().split('@')[0]
                resident = Resident.objects.get(kerberos=kerberos)
                if resident:
                    if not resident.user:
                        user = auth.models.User(username=kerberos)
                        user.save()
                        resident.user = user
                        resident.save()
                    resident.user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth.login(request, resident.user)
                    return redirect('profile')
            return redirect('home')
        token = get_random_string(length=32)
        request.session['token'] = token
        return redirect('{}?token={}'.format(settings.SCRIPTS_AUTH_URL, token))

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
