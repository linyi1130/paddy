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
    url(r'^result_l1/', result_l1),
    url(r'^result_post/', result_post),
    url(r'^result_union/', result_union),
    url(r'^result_unionbyclub/', result_unionbyclub),
    url(r'^useraccountview/', useraccountview),
    url(r'^usercash/', usercash),
    url(r'^login/', login),
    url(r'^default/', default),
    url(r'^report_view/', report_view),
    url(r'^operator/', operator),
    url(r'^add_operator_group/', add_operator_group),
    url(r'^operator_group_list/', operator_group_list),
    url(r'^operator_list/', operator_list),
    url(r'^add_operator/', add_operator),
    url(r'^operator_setup/', operator_setup),
    url(r'^operator_relation/', operator_relation),
    url(r'^operator_relation_setup/', operator_relation_setup),
    url(r'^relation_list/', relation_list),
    url(r'^club_account_info/', club_account_info),
    url(r'^check_balance/', check_balance),
    url(r'^test/', test),
    url(r'^searchUser/', searchUser),
    url(r'^modify_user/', modify_user),
    url(r'^modifyUserInfo/', modifyUserInfo),
    url(r'^user_account_group/', user_account_group),
    url(r'^user_group_search/', user_group_search),
    url(r'^account_migrate/', account_migrate),
    url(r'^club_manage/', club_manage),
    url(r'^club_info/', club_info),
    url(r'^modify_club/', modify_club),
]
