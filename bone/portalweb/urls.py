"""portalweb URL Configuration

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
from . import views, auth

urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^login/$', auth.login_view, name='login'),
    url(r'^logout/$', auth.logout_view, name='logout'),
    url(r'^quotes/new/$', views.quotes_new, name='quotes_new'),
    url(r'^quotes/(?P<quote_id>\d+)/delete/$', views.quotes_delete, name='quotes_delete')
]
