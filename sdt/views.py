from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from django.template import Context,Template
from django.template import loader
from django.http import HttpResponseRedirect
from sdt.models import *
from sdt.sdt_func import *
from .form import *
# Create your views here.
def club_list(request):

    t_club = ucs_subs_club.objects.all().order_by('-active_time')

    return render(request,'club.html',{'t_club':t_club})


def club_add(request):
    tmp=ucs_subs_club(club_name=request.POST['club_name'],
                      club_shortname=request.POST['short_name'],
                      income_rate=request.POST['income_rate'],
                      club_desc=request.POST['club_desc'],
                      insure_rate=request.POST['insure_rate'],
                      )
    tmp.save()
    return HttpResponseRedirect('/club/')

def checkclub(request):
    club_name=request.POST['club_name']
    message=False
    try:
        t=ucs_subs_club.objects.filter(club_name=club_name).exists()
        if t==True:
            message=False
        else:
            message=True
        return HttpResponse(message)
    except Exception as e:

        message=False

    return HttpResponse(message)

def user_add(request):
    t_user_name=request.POST['user_name']
    t_wx_name = request.POST['wx_name']
    #t_club_name = request.POST['club_name']
    t_note = request.POST['note']
    t_club_id = request.POST['club_id']
    try:
        #filterresult = real_user.objects.filter(user_name=t_user_name)
        filterresult = ucs_subs_user.objects.filter(inactive_time="2037-01-01")
        #filterresult.filter(user_name=t_user_name)
        if  len(filterresult.filter(user_name=t_user_name))>0:
            return HttpResponse(filterresult.values())
        else:
            user_reg(t_user_name,t_wx_name,t_club_id,t_note)
            return HttpResponseRedirect('/user')
    except Exception as e:
        return HttpResponse(e)
    return HttpResponseRedirect('/user')

def user_list(request):
    #t = loader.get_template('user_reg.html')
    #t_user = ucs_subs_user.objects.all()
    tb_user= SQL_user_list()
    tb_club=ucs_subs_club.objects.all()
    return render(request,'user.html',{'tb_user':tb_user,'tb_club':tb_club})

