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
    message=0
    try:
        t=ucs_subs_club.objects.filter(club_name=club_name).exists()
        if t==True:
            message=0
        else:
            message=1
        return HttpResponse(message)
    except Exception as e:

        message=0

    return HttpResponse(message)

def user_add(request):
    t_user_name=request.POST['user_name']
    t_wx_name = request.POST['wx_name']
    #t_club_name = request.POST['club_name']
    t_note = request.POST['note']
    t_club_id = request.POST['club_id']
    flag=False
    try:
        #filterresult = real_user.objects.filter(user_name=t_user_name)
        #filterresult = ucs_subs_user.objects.filter(inactive_time="2037-01-01")
        #tmp=filterresult.filter(user_name=t_user_name)
        old_user_id=ucs_subs_user.objects.filter(inactive_time="2037-01-01").get(user_name=t_user_name).user_id
        result=user_old_reg(old_user_id,t_club_id)
        if result==True:
            flag=True
        else:
            return HttpResponse("用户已存在")
    except Exception as e:
        user_reg(t_user_name, t_wx_name, t_club_id, t_note)
        flag=True

    return HttpResponseRedirect('/user')

def user_list(request):
    #t = loader.get_template('user_reg.html')
    #t_user = ucs_subs_user.objects.all()
    tb_user= SQL_user_list()
    tb_club=ucs_subs_club.objects.all()
    return render(request,'user.html',{'tb_user':tb_user,'tb_club':tb_club})

def cash(request):
    tb_user = SQL_user_list()
    try:
        acc_list=request.POST['acc_list']
    except Exception as e:
        acc_list=None
    return render(request,'cash.html',{'acc_list':acc_list,'tb_user':tb_user})

def getbalance(request):
    try: user_id=request.POST['user_id']
    except Exception as e:
        return  e

    #获取账户id
    account_id=ucs_subs_user.objects.filter(user_id=user_id).get(inactive_time='2037-01-01').account_id
    try:#暂时用第一个俱乐部当现有俱乐部
        balancenum=ucs_balance.objects.filter(account_id=account_id).filter(inactive_time='2037-01-01') \
                       .filter(club_id="1000").order_by('-updatetime')[0].balance/1000
    except Exception as e:
        balancenum=0
    return HttpResponse(balancenum)

def cashin(request):

    if request.POST.get('cashInOut',0)==0:
        isCashin="off"
    else:
        isCashin="on"
    chance=int(float(request.POST['cash_num'])*1000)
    #account_id=getaccIDwithUserid(request.POST['account_id'])
    user_id=request.POST['user_id']
    tmp=getBalancebyuid(user_id)
    balance=tmp[0]
    account_id=tmp[1]
    if isCashin=='on':
        chance=chance*-1
        chance_desc="客服结算"
    else:
        chance_desc="客服存款"

    if balance is not None:
        t=ucs_balance(account_id=account_id,
                    user_id=request.POST['user_id'],
                    club_id="1000",
                    balance=balance+chance,
                    chance=chance,
                    chance_desc=chance_desc
                  )
    else:
        t = ucs_balance(account_id=account_id,
                        user_id=request.POST['user_id'],
                        club_id='1000',
                        balance=chance,
                        chance=chance,
                        chance_desc=chance_desc
                        )
    t.save()
    acc_list = getBalanceList(account_id)
    tb_user = SQL_user_list()
    #return HttpResponseRedirect('/cash', {'acc_list':acc_list,'tb_user':tb_user})
    return render(request, 'cash.html', {'acc_list':acc_list,'tb_user':tb_user})

def result(request):
    t=loader.get_template('result.html')
    web_page=t.render()
    return HttpResponse(web_page)

def result_split(request):
    strResult=request.POST['result']
    gameno=request.POST['gameno']
    tb_result=result_reg(strResult,gameno)

    return render(request,'result_preview.html',{'tb_result':tb_result})

def result_pretreat_step1(request):
    strResult=request.POST['result']
    gameno=request.POST['gameno']
    result_preload(strResult,gameno)
    #返回新未注册玩家名单
    newuser=result_regNewUser(gameno)
    t_club = ucs_subs_club.objects.all().order_by('-active_time')
    return render(request,'result_newuser.html',{'newuser':newuser,'t_club':t_club})

def show(request):
    tmp=request.POST
    newuser=[]
    for key in tmp:
        newuser.append(tmp[key])
    lenlist=len(newuser)
    i=0
    while(i<lenlist):
        if user_reg(newuser[i],newuser[i],newuser[i+1],"")==True:
            i=i+2



    HttpResponse(tmp)