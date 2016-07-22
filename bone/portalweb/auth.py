from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
import hmac
import hashlib

from django.shortcuts import render, redirect
from boneweb.models import Resident

from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.utils.crypto import get_random_string

class ScriptsAuthenticationBackend(ModelBackend):
    def authenticate(self, token="", email="", signature=""):
        if self._verify_token(token, email, signature):
            kerberos = self._extract_kerberos(email)
            try:
                user = User.objects.get(username=kerberos)
            except User.DoesNotExist:
                try:
                    resident = Resident.objects.get(kerberos=kerberos)
                    user = User(username=kerberos)
                    user.save()
                    resident.user = user
                    resident.save()
                except:
                    return None
            return user
        return None

    @staticmethod
    def _verify_token(token, email, signature):
        if not email.lower().endswith('@mit.edu'):
            return False
        message = "{}:{}".format(token, email).encode('utf-8')
        h = hmac.new(settings.SCRIPTS_AUTH_KEY, message, hashlib.sha256)
        return hmac.compare_digest(h.hexdigest(), signature)

    @staticmethod
    def _extract_kerberos(email):
        return email.lower().split('@')[0]

def login_view(request):
    if request.user.is_authenticated():
        return redirect('profile')
    email = request.GET.get('email')
    signature = request.GET.get('signature')
    token = request.session.get('token')
    if email and signature and token:
        del request.session['token']
        user = authenticate(token=token, email=email, signature=signature)
        if user:
            login(request, user)
            return redirect('profile')
        return render(request, 'portalweb/authentication_failed.html')
    token = get_random_string(length=32)
    request.session['token'] = token
    return redirect('{}?token={}'.format(settings.SCRIPTS_AUTH_URL, token))

def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('home')
