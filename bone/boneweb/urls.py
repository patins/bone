"""boneweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^residents/$', views.residents, name='residents'),
    url(r'^residents/([0-9]{4})/$', views.residents_by_year, name='residents_by_year'),
    url(r'^residents/alumni/$', views.alumni, name='alumni'),
    url(r'^quotes/$', views.quotes, name='quotes')
    #url(r'^residents/([0-9]{4})/([A-Za-z0-9]+)/$', views.resident, name='resident'),
    #url(r'^residents/([0-9]{4})/([A-Za-z0-9]+)/image$', views.resident_image, name='resident_image'),
]
