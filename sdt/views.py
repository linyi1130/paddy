from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from django.template import Context,Template
from django.template import loader
from django.http import HttpResponseRedirect
from sdt.models import *
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