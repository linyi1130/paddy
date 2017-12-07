from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import render,HttpResponse
from django.template import Context,Template
from django.template import loader
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from sdt.models import *
from sdt.sdt_func import *
from .form import *
import datetime
# Create your views here.
def club_list(request):
    t_club = ucs_subs_club.objects.all().order_by('-active_time')
    return render(request, 'club.html', {'t_club': t_club})


def club_add(request):
    club_name=request.POST['club_name']
    club_shortname = request.POST['short_name']
    income_rate = request.POST['income_rate']
    club_desc = request.POST['club_desc']
    insure_rate = request.POST['insure_rate']
    tmp = ucs_subs_club(club_name = club_name.strip(),
                      club_shortname = club_shortname.strip(),
                      income_rate = income_rate.strip(),
                      club_desc = club_desc.strip(),
                      insure_rate = insure_rate.strip()
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
        user_reg(t_user_name.strip(), t_wx_name.strip(), t_club_id, t_note)
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
    operator_info=request.session['operator_info']
    operator_name=operator_info['operator_name']
    club_name=operator_info['club_name']
    group_name=operator_info['group_name']
    return render(request, 'cash.html', {'tb_user': tb_user,'operator_name':operator_name,
                                         'club_name':club_name, 'group_name':group_name})

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
    strResult = request.POST['result']
    gameno = request.POST['gameno']
    tb_result=result_reg(strResult,gameno)

    return render(request, 'result_preview.html', {'tb_result': tb_result})

def result_pretreat_step1(request):
    strResult = request.POST['result']
    gameno = request.POST['gameno']
    tmp_result.objects.filter(game_no=gameno).delete()
    result_preload(strResult, gameno)
    # 返回新未注册玩家名单
    newuser = result_regNewUser(gameno)
    if len(newuser) > 0:
        t_club = ucs_subs_club.objects.all().order_by('-active_time')

        #return HttpResponseRedirect(request,'/result_newuser/',{'newuser':newuser,'t_club':t_club,'gameno':gameno})
        return render_to_response('result_newuser.html',{'newuser':newuser,'t_club':t_club,'gameno':gameno})
    else:
        split_club=result_attachclub(gameno)
        if len(split_club)>0 :
            return render(request, 'result_attachclub.html', {'row': split_club, 'gameno': gameno})
    #没有新增玩家和待选择俱乐部，直接进入战绩预览
    return None
def result_newuser(request):
    tmp = request.POST
    newuser = []
    gameno=request.POST['gameno']

    for key in tmp:
        if key != "gameno" :
            newuser.append(tmp[key])
    lenlist = len(newuser)
    i = 0
    while (i < lenlist):
        if user_reg(newuser[i],newuser[i],newuser[i+1],"") == True :
            i=i+2
        i=i+2
    split_club = result_attachclub(gameno)
    if len(split_club) > 0:
        return render(request, 'result_attachclub.html', {'row': split_club, 'gameno': gameno})

    return HttpResponseRedirect('/result_club/', {'gameno' : gameno })  #要进入战绩预览，这里要改

def result_club(request):  #处理多俱乐部玩家
    tmp_split=request.POST
    gamono=request.POST['gameno']
    flag = split_club(tmp_split)
    if flag==True:
        #url=reverse(result_preview,kwargs={'gameno':gamono})
        url="/result_preview/?gameno=" + gamono
        #render(request, "/result_preview/", {'gamono':gamono})
        return HttpResponseRedirect(url)
    else:
        return HttpResponse("出错啦！")

def result_preview(request):
    gamono = request.GET.get('gameno')
    result=result_reg(gamono)
    return render(request,'result_preview.html',{'tb_result':result, 'gameno':gamono})
def loadtabletype(request):
    gametype=pm_gametype.objects.all()
    blind=pm_blind.objects.all()
    gametime=pm_gametime.objects.all()
    gamepeople=pm_gamepeople.objects.all()

    return render(request, 'table.html', {'gametype':gametype,'blind':blind,"gametime":gametime,"gamepeople":gamepeople})

def result_view(request):
    t_club = ucs_subs_club.objects.all().order_by('-active_time')
    t_game_list=gamenolist()

    return render(request,"resultview.html", {'t_club': t_club,'t_game_list': t_game_list})

def result_l1(request):
    club_id=request.POST['club_id']
    club_name=request.POST['club_name']
    startdate=request.POST['start']
    enddate=request.POST['end']
    tb_result=result_searchByclub(club_id,startdate,enddate)
    tb_sum = result_searchByclubSum(club_id,startdate,enddate)
    return  render(request,'result_l1.html',{'tb_result':tb_result, 'club_name': club_name,'tb_sum' : tb_sum } )

def result_post(request):
    gameno= request.POST['gameno']
    flag=result_record(gameno)
    if flag:
        return HttpResponse('/result_l1/')
    else :
        return HttpResponse("添加失败")

def result_union(request):

    return render(request, "result_union.html")

def result_unionbyclub(request):
    startime=request.POST['start']
    endtime=request.POST['end']
    tb_result=result_searchUnionbyclub(startime,endtime)
    tb_result_sum = result_searchUnionbyclubsum(startime,endtime)
    return  render(request, "result_unionbyclubl1.html", {'tb_result': tb_result,'starttime':startime,'endtime':endtime,'tb_result_sum': tb_result_sum })

def useraccountview(request):
    account_id=request.POST['account_id']
    user_name=request.POST['user_name']
    club_id='1000'
    tb_result=getUserAccountInfo(account_id,club_id)
    tb_balance_list=getUserBalenceList(account_id,club_id)
    club_name="荣耀联盟"
    return render(request, 'user_account_info.html',{'user_name':user_name,'tb_result':tb_result,
                                                     'club_name':club_name,'tb_balance_list':tb_balance_list})

def usercash(request):
    user_id=request.POST['user_id']
    account_id=request.POST['account_id']
    club_id='1000'
    operator_id='3001'
    club_name = "荣耀联盟"
    user_name=request.POST['user_name']
    change_num=int(float(request.POST['change_num'])*1000)
    chang_type=request.POST['change_type'],
    note=request.POST['note']
    if chang_type[0] == "false":
        cashtype=0
    else: cashtype=1
    result=userCashReg(account_id, user_id, club_id, cashtype, operator_id,change_num,note)
    if result==True:
        tb_result = getUserAccountInfo(account_id, club_id)
        tb_balance_list = getUserBalenceList(account_id, club_id)
        return render(request, 'user_account_info.html',{'user_name':user_name,'tb_result':tb_result,
                                                     'club_name':club_name,'tb_balance_list':tb_balance_list})
    else: HttpResponse("出错啦！")
    return HttpResponse("/cash/")


def default(request):
    request.session.set_expiry(0)
    request.session.clear_expired()
    return render(request,"login.html")

def report_view(request):

    return render(request,"report_navigate.html")

def operator(request):
    #group_list=ucs_operator_group.objects.all()
    return render(request,'manage/operator_manage.html')

def operator_setup(request):
    club_id='1000'
    tb_group_list = ucs_operator_group.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)
    tb_operator_list = ucs_operator.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)
    return render(request, 'manage/operator_setup.html', {'tb_group_list':tb_group_list, 'tb_operator_list':tb_operator_list})

def operator_group_list(request):
    club_id='1000'
    tb_group_list = ucs_operator_group.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)
    return render(request, 'manage/group_list.html', {'tb_group_list':tb_group_list})

def add_operator_group(request):
    group_name=request.POST['group_name']
    club_id='1000'
    message=add_group(group_name, club_id)
    if message:
        cnt = 1
        while cnt <= 3:
            account_id=create_club_accountID(club_id)
            if create_club_account(account_id,club_id,cnt,message):
                cnt = cnt + 1
    return render(request, 'manage/group_list.html')


def operator_list(request):
    club_id='1000'
    tb_operator_list = ucs_operator.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)
    return render(request,'manage/operator_list.html', {'tb_operator_list' : tb_operator_list})

def add_operator(request):
    operator_name=request.POST['operator_name']
    login_id=request.POST['login_id']
    club_id='1000'
    message=add_operator_func(operator_name, login_id, club_id)
    return render(request, 'manage/operator_list.html')

def operator_relation(request):
    club_id='1000'
    tb_group_list = ucs_operator_group.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)
    tb_operator_list = ucs_operator.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id).filter(group_id=None)
    tb_relation = operator_relation_list(club_id)
    return render(request, 'manage/operator_relation.html', {'tb_group_list':tb_group_list,
                                                             'tb_operator_list':tb_operator_list})

def relation_list(request):
    club_id='1000'
    tb_relation = operator_relation_list(club_id)
    return render(request, 'manage/relation_list.html',{'tb_relation':tb_relation})


def operator_relation_setup(request):
    operator_id_list = request.POST['operator_id']
    group_id = request.POST['group_id']
    operator_id=operator_id_list.split(",")
    for t in operator_id:
        if t != "":
            try:
                t=ucs_operator.objects.filter(inactive_time='2037-01-01').get(operator_id=t)
                t_operator_id=t.operator_id
                t_operator_name=t.operator_name
                t_club_id=t.club_id
                t_login_id=t.login_id
                t_password=t.password
                t.inactive_time=datetime.datetime.now()
                t.save()
                p=ucs_operator(operator_id=t_operator_id,
                               operator_name=t_operator_name,
                               club_id=t_club_id,
                               group_id=group_id,
                               login_id=t_login_id,
                               password=t_password,
                               active_time=datetime.datetime.now())
                p.save()
            except Exception as e:
                return e
    return HttpResponseRedirect('/operator_relation/')

def login(request):
    login_id=request.POST['login_id']
    password=request.POST['password']
    result =operator_login (login_id, password)
    if result:
        request.session['operator_info']=result
        return HttpResponseRedirect('/cash/')
    else:
        return HttpResponse("用户名或密码不匹配")

