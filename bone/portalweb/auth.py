from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from boneweb.models import Resident

from django.conf import settings
from django.contrib.auth import login, logout, authenticate

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
    print(request.META)
    email = request.META.get('HTTP_EPPN')
    if email:
        user = authenticate(email=email)
        if user:
            login(request, user)
            return redirect('profile')
        return render(request, 'portalweb/authentication_failed.html')
    target_uri = request.build_absolute_uri(request.path)
    redirect_qs = urlencode({'target': target_uri})
    return redirect("{}?{}".format(settings.SHIB_LOGIN_URL, redirect_qs))

def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('home')
