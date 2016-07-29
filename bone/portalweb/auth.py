from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.http import HttpResponse
from boneweb.models import Resident

from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse

from urllib.parse import urlencode

class ShibbolethAuthenticationBackend(ModelBackend):
    def authenticate(self, email=""):
        if self._verify_email(email):
            kerberos = self._extract_kerberos(email)
            try:
                user = User.objects.get(username=kerberos)
            except User.DoesNotExist:
                try:
                    resident = Resident.objects.get(kerberos=kerberos) #ONLY MAKE IF USER EXISTS
                    user = User(username=kerberos)
                    user.save()
                    resident.user = user
                    resident.save()
                except:
                    return None
            return user
        return None

    @staticmethod
    def _verify_email(email):
        return email.lower().endswith('@mit.edu')

    @staticmethod
    def _extract_kerberos(email):
        return email.lower().split('@')[0]

def login_view(request):
    if request.user.is_authenticated():
        return redirect('profile')
    email = request.META.get('HTTP_EPPN')
    if settings.DEBUG and settings.SHIB_RESPONDER_URL is None:
        email = request.GET.get('eppn')
    if email:
        user = authenticate(email=email)
        if user:
            login(request, user)
            return redirect('profile')
        return render(request, 'portalweb/authentication_failed.html')
    if settings.SHIB_RESPONDER_URL is None:
        if settings.DEBUG:
            return HttpResponse("No shib to redirect to. Use ?eppn=<email>")
        else:
            return render(request, 'portalweb/authentication_failed.html')
    target_uri = request.build_absolute_uri(request.path)
    redirect_qs = urlencode({'target': target_uri})
    return redirect("{}/Login?{}".format(settings.SHIB_RESPONDER_URL, redirect_qs))

def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
        if settings.SHIB_RESPONDER_URL:
            home_uri = request.build_absolute_uri(reverse('home'))
            redirect_qs = urlencode({'return': home_uri})
            return redirect("{}/Logout?{}".format(settings.SHIB_RESPONDER_URL, redirect_qs))
    return redirect('home')
