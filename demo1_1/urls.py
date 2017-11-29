"""demo1_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib import admin
from sdt.views import *
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^club/', club_list),
    url(r'^club_add/', club_add),
    url(r'^checkclub/', checkclub),
    url(r'^user/',user_list),
    url(r'^user_add/',user_add),
    url(r'^cash/',cash),
    url(r'^getbalance/',getbalance),
    url(r'^cashin/',cashin),
    url(r'^result/', result),
    url(r'^result_pretreat_step1/', result_pretreat_step1),
    url(r'^result_newuser/', result_newuser),
    url(r'^result_club/', result_club),
    url(r'^table/', loadtabletype),
    url(r'^result_preview/$', result_preview),
    url(r'^result_view/', result_view),
]
