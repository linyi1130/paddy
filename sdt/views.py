from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import render,HttpResponse
from django.template import Context,Template,RequestContext
from django.template import loader
from django.http import HttpResponseRedirect,HttpResponse
from sdt.models import *
from sdt.sdt_func import *
import datetime
import json
import django.core.serializers.json
from django.forms.models import model_to_dict
from django.core import serializers
import os
from django.conf import settings
# Create your views here.
def loadsidebar(request):

    return render(request,'sidebar.html')


def loadnavigate(request):

    return render(request,'web_navigate.html')


def club_list(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    if not permission.filter(type_id=8).exists():
        return HttpResponseRedirect('/warning/')
    club_id=operator_info['club_id']
    t_club = getCLubList(club_id)
    if len(t_club)==0:
        insure_rate = 100
        income_rate = 100
    else:
        try:
            club_info=ucs_subs_club.objects.filter(inactive_time='2037-01-01').get(club_id=club_id)
            income_rate=club_info.income_rate
            insure_rate=club_info.insure_rate
        except:
            insure_rate=0
            income_rate=0
    return render(request, 'club.html', {'t_club': t_club,'income_rate': income_rate,'insure_rate': insure_rate})


def club_add(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    club_id=operator_info['club_id']
    club_level = operator_info['club_level']
    if club_level>4:
        return False
    subs_club_level=int(club_level)+1
    club_name=request.POST['club_name']
    club_shortname = request.POST['short_name']
    income_rate = request.POST['income_rate']
    club_desc = request.POST['club_desc']
    insure_rate = request.POST['insure_rate']
    #注册成功返回ID
    subs_club_id=club_reg(club_name, club_shortname,club_desc, income_rate, insure_rate,subs_club_level )
    if subs_club_id:
        #加入俱乐部关系表
        t=ucs_club_relation(club_id=club_id,
                          subs_club_id=subs_club_id,
                            club_level=club_level)
        t.save()
        return HttpResponseRedirect('/club/')
    else:
        result=False
        return HttpResponse(result)

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

def checkuser(request):
    user_name=request.POST['user_name']
    club_id=request.POST['club_id']
    result=checkUserExist(user_name, club_id)
    return HttpResponse(result)


def user_add(request):
    operator_info=request.session['operator_info']
    operator_id=operator_info['operator_id']
    user_name=request.POST['user_name']
    wx_name=request.POST['wx_name']
    note=request.POST['note']
    club_id=request.POST['club_id']
    result=checkUserExist(user_name,club_id)
    if result==0:
        flag=user_reg(user_name, wx_name, club_id, note,operator_id)

        return HttpResponse(flag)

    else:
        return HttpResponse("False")

def old_user_add(request):
    user_name=request.POST['user_name']
    club_id=request.POST['club_id']
    result=user_old_reg(user_name, club_id)
    return HttpResponse(result)




def user(request):
    #t = loader.get_template('user_reg.html')
    #t_user = ucs_subs_user.objects.all()
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    if not permission.filter(type_id=1).exists():
        return HttpResponseRedirect('/warning/')
    club_id=operator_info['club_id']
    tb_club=ucs_subs_club.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)
    return render(request,'user.html',{'tb_club':tb_club})

def user_list(request):
    club_id=request.POST['club_id']
    tb_result=getUserListByClubId(club_id)
    return render(request, 'user_list.html',{'tb_user': tb_result})

#初始化充值页面
def cash(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    if not permission.filter(type_id=1).exists():
        return HttpResponseRedirect('/warning/')
    operator_name=operator_info['operator_name']
    club_name=operator_info['club_name']
    club_id = operator_info['club_id']
    group_id = operator_info['group_id']
    group_name=operator_info['group_name']
    tb_user = SQL_user_list(club_id)
    tb_type_list=ucs_club_account.objects.filter(inactive_time='2037-01-01').filter(group_id=group_id).filter(club_id=club_id).values('account_id','account_desc')
    return render(request, 'cash2.html', {'tb_user': tb_user,'operator_name':operator_name,
                                         'club_name':club_name, 'group_name':group_name, 'tb_type_list': tb_type_list})


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

#作废
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
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    if not permission.filter(type_id=7).exists():
        return HttpResponseRedirect('/warning/')
    game_no=request.GET.get('game_no')

    return render(request,'result.html',{'game_no':game_no})


def result_split(request):
    strResult = request.POST['result']
    gameno = request.POST['gameno']
    tb_result=result_reg(strResult,gameno)

    return render(request, 'result_preview.html', {'tb_result': tb_result})


def result_pretreat_step1(request):
    strResult = request.POST['result']
    gameno = request.POST['gameno']
    tmp_result.objects.filter(game_no=gameno).delete()
    tmp_result_attachclub_pre.objects.filter(gameno=gameno).delete()
    if result_preload(strResult, gameno):
    # 返回新未注册玩家名单
        newuser = result_regNewUser(gameno)
        if newuser:
            t_club = ucs_subs_club.objects.filter(inactive_time='2037-01-01').order_by('-active_time')

            #return HttpResponseRedirect(request,'/result_newuser/',{'newuser':newuser,'t_club':t_club,'gameno':gameno})
            return render_to_response('result_newuser.html',{'newuser':newuser,'t_club':t_club,'gameno':gameno})
        else:
            split_club=result_attachclub(gameno)
            if len(split_club)>0 :
                return render(request, 'result_attachclub.html', {'row': split_club, 'gameno': gameno})
        #没有新增玩家和待选择俱乐部，直接进入战绩预览
        url = "/result_preview?gameno=" + gameno + "&type=1"
        return HttpResponseRedirect(url)
    else:
        return HttpResponse("原始战绩不完整，请重新导入")
def result_newuser(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id=operator_info['operator_id']
    tmp = request.POST
    newuser = []
    gameno=request.POST['gameno']

    for key in tmp:
        if key != "gameno" :
            newuser.append(tmp[key])
    lenlist = len(newuser)
    i = 0
    while (i < lenlist):
        if user_reg(newuser[i],newuser[i],newuser[i+1],"",operator_id) == True :
            i=i+2
        #i=i+2
    split_club = result_attachclub(gameno)
    if len(split_club) > 0:
        return render(request, 'result_attachclub.html', {'row': split_club, 'gameno': gameno})
    url="/result_preview?gameno="+gameno + "&type=1" #1表示俱乐部匹配未完成
    return HttpResponseRedirect(url)

def result_club(request):  #处理多俱乐部玩家
    tmp_split=request.POST
    gamono=request.POST['gameno']
    flag = split_club(tmp_split)
    if flag==True:
        #url=reverse(result_preview,kwargs={'gameno':gamono})
        url="/result_preview/?gameno=" + gamono + "&type=2"   #2表示俱乐部匹配已经完成
        #render(request, "/result_preview/", {'gamono':gamono})
        return HttpResponseRedirect(url)
    else:
        return HttpResponse("出错啦！")

def result_preview(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    if not permission.filter(type_id=7).exists():
        return HttpResponseRedirect('/warning/')
    gameno = request.GET.get('gameno')
    type=request.GET.get('type')
    if type=="1":
        tmp_split={'gameno': gameno}
        flag=split_club(tmp_split)
        if flag:
            result = result_reg(gameno)
            return render(request, 'result_preview.html', {'tb_result': result, 'gameno': gameno})
    elif type=="2":
        result = result_reg(gameno)
        return render(request,'result_preview.html',{'tb_result':result, 'gameno':gameno})


def loadtabletype(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    if not permission.filter(type_id=7).exists():
        return HttpResponseRedirect('/warning/')
    gametype=pm_gametype.objects.all()
    blind=pm_blind.objects.all()
    gametime=pm_gametime.objects.all()
    gamepeople=pm_gamepeople.objects.all()
    ante=pm_ante.objects.filter(blind_id=1).order_by('id')
    return render(request, 'table.html', {'gametype':gametype,'blind':blind,"gametime":gametime,"gamepeople":gamepeople, "ante":ante})

def getante(request):
    blind_id=request.POST['blind_id']
    tmp=getAnteList(blind_id)
    ante_list = json.dumps(tmp, cls=django.core.serializers.json.DjangoJSONEncoder)
    return HttpResponse(ante_list)

def table_list(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    if not permission.filter(type_id=2).exists():
        return HttpResponseRedirect('/warning/')
    permission_flag=permission.filter(type_id=7).exists()
    tb_result=getTableList()
    return render(request,'table_list.html', {'table_list': tb_result,'permission_flag':permission_flag})


def game_reg(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id=operator_info['operator_id']
    permission = getPermission(operator_id)
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    if not permission.filter(type_id=7).exists():
        return HttpResponseRedirect('/warning/')
    group_name=operator_info['group_name']
    blind=request.POST['blind']
    gametype=request.POST['gametype']
    ante=request.POST['ante']
    duration=request.POST['duration']
    straddle_tmp=request.POST['straddle']
    if straddle_tmp=="true":
        straddle=1
    else:straddle=0
    game_no=createGameNo(gametype,blind,ante)
    if game_no:
        result=gameRegFunc(game_no,gametype,blind,ante,straddle,0,duration,now(),1,"进行中",operator_id,group_name)
        return HttpResponse(result)
    result=False
    return HttpResponse(result)

def result_view(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    if not permission.filter(type_id=4).exists():
        return HttpResponseRedirect('/warning/')
    t_club = getClubListMini()
    return render(request,"resultview.html", {'t_club': t_club})

def result_l1(request):
    club_id=request.POST['club_id']
    club_name=request.POST['club_name']
    startdate=request.POST['start']
    enddate=request.POST['end']
    tb_result=result_searchByclub(club_id,startdate,enddate)
    tb_sum = result_searchByclubSum(club_id,startdate,enddate)
    return  render(request,'result_l1.html',{'tb_result':tb_result, 'club_name': club_name,'tb_sum' : tb_sum,'club_id':club_id } )

def result_post(request):
    gameno= request.POST['gameno']
    operator_info = request.session['operator_info']
    club_id=operator_info['club_id']
    group_id=operator_info['group_id']
    operator_id=operator_info['operator_id']
    flag=result_record(gameno,operator_id,club_id )
    if flag:
        seriale_no = createSerialNo(club_id, group_id, 1003)
        t1=gameResultClubReg(gameno,club_id, group_id, operator_id,seriale_no)
        t2=gameResultUserReg(gameno,club_id,operator_id,seriale_no)
        if t1 & t2:
            regedGameByNo(gameno)
            tb_result = []
            club_list = ucs_result_table.objects.filter(inactive_time='2037-01-01').filter(game_no=gameno) \
                .values('club_id').distinct()
            for t in club_list:
                club_id = t['club_id']
                tb_result.append(getResultDetailByGameno(gameno, club_id))
            return render(request, 'result_detail_tb.html', {'tb_result': tb_result})
    else :
        return HttpResponse("添加失败")

def result_detail(request):
    gameno=request.POST['game_no']

    club_list = ucs_result_table.objects.filter(inactive_time='2037-01-01').filter(game_no=gameno) \
            .values('club_id').distinct()
    tb_result=[]
    for t in club_list:
        club_id=t['club_id']
        tb_result.append(getResultDetailByGameno(gameno, club_id))
    return render(request, 'result_detail_tb.html', {'tb_result': tb_result})


def result_detailbyClub(request):
    gameno = request.POST['game_no']
    club_id=request.POST['club_id']
    tb_result=[]
    tb_result.append(getResultDetailByGameno(gameno, club_id))
    return render(request, 'result_detail_tb.html', {'tb_result': tb_result})


def result_union(request):
    operator_info = request.session['operator_info']
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    if not permission.filter(type_id=4).exists():
        return HttpResponseRedirect('/warning/')
    return render(request, "result_union.html")


def result_unionbyclub(request):
    operator_info = request.session['operator_info']
    club_id=operator_info['club_id']
    startime=request.POST['start']
    endtime=request.POST['end']
    tb_result=result_searchUnionbyclub(startime,endtime,club_id)
    tb_result_sum = result_searchUnionbyclubsum(startime,endtime,club_id)
    return  render(request, "result_unionbyclubl1.html", {'tb_result': tb_result,'starttime':startime,'endtime':endtime,'tb_result_sum': tb_result_sum })


def useraccountview(request):
    operator_info = request.session['operator_info']
    account_id=request.POST['account_id']
    user_id=request.POST['user_id']
    user_name=request.POST['user_name']
    club_id=operator_info['club_id']
    tb_result=getUserAccountInfo(account_id,club_id)
    tb_developer = getUserDeveloperByUserId(user_id, club_id)
    if len(tb_developer) >0:
        tb_result['developer_name'] = tb_developer[0][1]
    else:tb_result['developer_name'] = ""
    tb_balance_list=getUserBalenceList(account_id,club_id)
    club_name=operator_info['club_name']
    tb_freeze=getFreezeListByUid(user_id, club_id)
    return render(request, 'user_account_info.html',{'user_name':user_name,'tb_result':tb_result,
                                                     'club_name':club_name,'tb_balance_list':tb_balance_list, 'tb_freeze':tb_freeze})
#玩家充值结算
def usercash(request):
    user_id=request.POST['user_id']
    account_id=request.POST['account_id']
    operator_info=request.session['operator_info']
    club_id=operator_info['club_id']
    operator_id=operator_info['operator_id']
    group_id=operator_info['group_id']
    club_name = operator_info['club_name']
    user_name=request.POST['user_name']
    change_num=int(float(request.POST['change_num'])*1000)
    chang_type=request.POST['change_type']
    note=request.POST['note']
    type_id=request.POST['pay_account']
    #operator_account_id = get_operator_accountID(club_id, group_id, type_id)
    if chang_type == "false":
        cashtype=1001  #客服充值
        serial_no = createSerialNo(club_id, group_id, cashtype)
        result=userCashReg(account_id, user_id, club_id, cashtype, operator_id, change_num, note,serial_no)
        if result: #用户充值成功
            flag=operator_cash(type_id, change_num, cashtype, operator_id, note,serial_no, group_id)
            if flag:
                tb_result = getUserAccountInfo(account_id, club_id)
                tb_developer = getUserDeveloperByUserId(user_id, club_id)
                if len(tb_developer) >0:
                    tb_result['developer_name'] = tb_developer[0][1]
                tb_balance_list = getUserBalenceList(account_id, club_id)
                return render(request, 'user_account_info.html', {'user_name': user_name, 'tb_result': tb_result,
                                                    'club_name':club_name, 'tb_balance_list': tb_balance_list})
            return HttpResponse("出错了")
        else: return HttpResponse("出错了")
    elif chang_type=='true':
        cashtype = 2001
        serial_no=createSerialNo(club_id, group_id,cashtype)
        result = userCashReg(account_id, user_id, club_id, cashtype, operator_id, change_num, note, serial_no)
        if result:  # 用户充值成功
            flag = operator_cash(type_id, change_num, cashtype, operator_id, note, serial_no,group_id)
            if flag:
                tb_result = getUserAccountInfo(account_id, club_id)
                tb_developer=getUserDeveloperByUserId(user_id,club_id)
                if len(tb_developer) >0:
                    tb_result['developer_name']=tb_developer[0][1]
                tb_balance_list = getUserBalenceList(account_id, club_id)
                return render(request, 'user_account_info.html', {'user_name': user_name, 'tb_result': tb_result,
                                                                  'club_name': club_name,
                                                                  'tb_balance_list': tb_balance_list})
            return HttpResponse("出错了")
        else:
            return HttpResponse("出错了")

    return HttpResponse("/cash/")


def default(request):
    request.session.set_expiry(0)
    request.session.clear_expired()
    return render(request,"login.html")


def report_view(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    if not permission.filter(type_id=4).exists():
        return HttpResponseRedirect('/warning/')
    return render(request,"report_navigate.html")


def operator(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id=operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission=getPermission(operator_id)
    if permission.filter(type_id=5).exists():
        return render(request,'manage/operator_manage.html')
    else:
        return HttpResponseRedirect('/warning/')


def operator_setup(request):
    operator_info=request.session['operator_info']
    club_id = operator_info['club_id']
    tb_group_list = ucs_operator_group.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)
    tb_operator_list = ucs_operator.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)
    return render(request, 'manage/operator_setup.html', {'tb_group_list':tb_group_list, 'tb_operator_list':tb_operator_list})


def operator_group_list(request):
    operator_info=request.session['operator_info']
    club_id = operator_info['club_id']
    tb_group_list = ucs_operator_group.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)
    return render(request, 'manage/group_list.html', {'tb_group_list':tb_group_list})

#新增客服组
def add_operator_group(request):
    group_name=request.POST['group_name']
    operator_info=request.session['operator_info']
    club_id = operator_info['club_id']
    message=add_group(group_name, club_id)
    if message:
        cnt = 1
        while cnt <= 3:
            account_id=create_club_accountID(club_id)
            serial_no=createSerialNo(club_id,1,1)
            account_type=pm_account_type.objects.filter(inactive_time='2037-01-01').get(type_id=cnt).type
            if create_club_account(account_id,club_id,cnt,message,account_type):
                operator_cash(account_id, 0, 9999, 9999, "初始化",serial_no, message)
                cnt = cnt + 1
    return render(request, 'manage/group_list.html')


def operator_list(request):
    operator_info=request.session['operator_info']
    club_id = operator_info['club_id']
    tb_operator_list = ucs_operator.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)
    return render(request,'manage/operator_list.html', {'tb_operator_list' : tb_operator_list})


def add_operator(request):
    operator_name=request.POST['operator_name']
    login_id=request.POST['login_id']
    operator_info=request.session['operator_info']
    club_id = operator_info['club_id']
    club_level=operator_info['club_level']
    if club_level==0:
        permission_id=106
    else:
        permission_id=103
    message=add_operator_func(operator_name, login_id, club_id,permission_id)
    return render(request, 'manage/operator_list.html')

def operator_relation(request):
    operator_info=request.session['operator_info']
    club_id = operator_info['club_id']
    tb_group_list = ucs_operator_group.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)
    tb_operator_list = ucs_operator.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id).filter(group_id=None)
    tb_relation = operator_relation_list(club_id)
    return render(request, 'manage/operator_relation.html', {'tb_group_list':tb_group_list,
                                                             'tb_operator_list':tb_operator_list})


def relation_list(request):
    operator_info=request.session['operator_info']
    club_id = operator_info['club_id']
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
                t_permission_group=t.permission_group
                t.inactive_time=datetime.datetime.now()
                t.save()
                p=ucs_operator(operator_id=t_operator_id,
                               operator_name=t_operator_name,
                               club_id=t_club_id,
                               group_id=group_id,
                               login_id=t_login_id,
                               password=t_password,
                               permission_group=t_permission_group,
                               active_time=datetime.datetime.now())
                p.save()
            except Exception as e:
                return e
    return HttpResponseRedirect('/operator_relation/')


def login(request):
    login_id=request.POST['login_id']
    password=request.POST['password']
    if login_id=="paddy":
        ps=paddy_admin.objects.get(login_name=login_id).password
        request.session['supper']='paddy'
        if check_password(password,ps):
            return HttpResponseRedirect("/app_initialize/")
    result =operator_login (login_id, password)
    if result:
        request.session['operator_info'] = result
        if result['is_active']==False:
            return HttpResponseRedirect('/operator_disable/')
        request.session['operator_info']=result
        return HttpResponseRedirect('/welcome/')
    else:
        return HttpResponse("用户名或密码不匹配")


def club_account_info(request):
    operator_info=request.session['operator_info']
    club_id = operator_info['club_id']
    group_id = operator_info['group_id']
    group_name=operator_info['group_name']
    tb_result=get_club_account_infoByGroup(club_id,group_id)
    tb_union_list=getUnionClubAccountList(club_id)
    return render(request, 'sidebar_account.html', {'tb_result': tb_result,'tb_union_list':tb_union_list, 'group_name': group_name})


def check_balance(request):
    operator_info = request.session['operator_info']
    account_id = request.POST['account_id']
    club_id = operator_info['club_id']
    #group_id = operator_info['group_id']
    type_id = request.POST['pay_account']
    change_num = int(float(request.POST['change_num']) * 1000)
    #operator_account_id = get_operator_accountID(club_id, group_id, type_id)
    user_balance = getBalancebyaid(account_id,club_id)
    if change_num>user_balance:
        msg=1
        return HttpResponse(msg)
    type_balance = get_club_balance_byType(type_id)
    if change_num>type_balance:
        msg=2
        return HttpResponse(msg)
    msg=True
    return HttpResponse(msg)

def welcome(request):

    return render(request,'notice.html')

def searchUser(request):
    user_name=request.POST['user_name']
    t=request.session['operator_info']
    club_id=t['club_id']
    tb_result=getUserInfoByName(user_name,club_id)
    if tb_result:
        #return HttpResponse(tb_result)
        tmp=json.dumps(tb_result)
        return HttpResponse(tmp)
        #return render(request,'user_modify.html',{'tb_result':tmp, 'user_name':user_name})
    else:
        message="没有匹配到玩家"
        return HttpResponse(message)
def modifyUserInfo(request):
    t=request.session['operator_info']
    club_id=t['club_id']
    user_id=request.POST['user_id']
    new_name=request.POST['user_name']
    new_wx_name=request.POST['wx_name']
    new_note=request.POST['note']
    old_name = request.POST['old_name']
    if old_name!=new_name:
        if checkUserNameExist(new_name):
            result=modifyUserInfoFunc(user_id, new_name, new_wx_name, new_note)
            if result:
                return HttpResponse(result)
        else:
            result="玩家名字已存在"
            return HttpResponse(result)
    else:
        result = modifyUserInfoFunc(user_id, new_name, new_wx_name, new_note)
        if result:
            return HttpResponse(result)

def modify_user(request):
    operator_info=request.session['operator_info']
    operator_id = operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission = getPermission(operator_id)
    if not permission.filter(type_id=9).exists():
        return HttpResponseRedirect('/warning/')
    club_id=operator_info['club_id']

    tb_user = getUserListByClubId(club_id)
    return render(request,'user_modify.html', {'tb_user':tb_user,'club_id': club_id})


def user_account_group(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission = getPermission(operator_id)
    if not permission.filter(type_id=9).exists():
        return HttpResponseRedirect('/warning/')
    club_id=operator_info['club_id']

    tb_user = getUserListWithOutDeveByClubId(club_id)
    return render(request, 'user_account_group.html', {'tb_user': tb_user, 'club_id': club_id})


def user_group_search(request):
    account_id=request.POST['account_id']
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    tb_account_info=getUserAccountInfo(account_id, club_id)
    result=json.dumps(tb_account_info, cls=django.core.serializers.json.DjangoJSONEncoder)
    return HttpResponse(result)


def account_migrate(request):
    o_account_id=request.POST['o_account_id']
    t_account_id=request.POST['t_account_id']
    t_user_id=request.POST['t_user_id']
    t_account_name=request.POST['t_account_name']
    t=request.session['operator_info']
    club_id=t['club_id']
    operator_id=t['operator_id']
    result=userAccountMigrate(o_account_id,t_account_id,t_account_name, t_user_id,club_id,operator_id)

    return HttpResponse(result)


def club_manage(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if not permission.filter(type_id=8).exists():
        return HttpResponseRedirect('/warning/')
    tb_club_list=getClubListMini()
    return render(request,'club_manage.html',{'tb_club_list': tb_club_list})


def club_info(request):
    club_id=request.POST['club_id']
    tb_club_list=getClubInfoById(club_id)
    result=json.dumps(model_to_dict(tb_club_list), cls=django.core.serializers.json.DjangoJSONEncoder)
    return HttpResponse(result)

def modify_club(request):
    club_id=request.POST['club_id']
    club_name=request.POST['club_name']
    club_shortname = request.POST['club_shortname']
    club_desc=request.POST['club_desc']
    income_rate=request.POST['income_rate']
    insure_rate=request.POST['insure_rate']
    result=modifyClubInfo(club_id, club_name,club_shortname, club_desc, income_rate, insure_rate)
    return HttpResponse(result)


def table_reg_mini(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    tb_user=getUserListByClubId(club_id)
    gameno=request.POST['gameno']
    try:
        status_id=ucs_gamerecord.objects.filter(inactive_time='2037-01-01').get(game_no=gameno).status_id
        if (status_id==4 or status_id==5):
            return HttpResponse('False')
    except:
        return HttpResponse('False')
    return render(request, 'buyinregsubs.html',{'tb_user': tb_user, 'gameno': gameno})


def getusefulbalance(request):
    account_id=request.POST['account_id']
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    balance=getBalancebyaid(account_id, club_id)
    freeze_sum=getFreezeSumByAid(account_id,club_id)
    balance_useful=round((balance-freeze_sum)/1000,2)
    return HttpResponse(balance_useful)


def userbuyin(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    operator_id=operator_info['operator_id']
    group_name = operator_info['group_name']
    account_id=request.POST['account_id']
    user_id=request.POST['user_id']
    freeze_num=request.POST['freeze_num']
    note=group_name+"登记上分"
    game_no=request.POST['game_no']
    freeze_num=int(float(freeze_num)*1000)
    try:
        tb_game_info=ucs_gamerecord.objects.filter(inactive_time='2037-01-01').get(game_no=game_no)
        start_time=tb_game_info.start_time
        #start_time=datetime.datetime.fromtimestamp(str_start_time)
        duration=int(tb_game_info.duration)
        unfreeze_time=start_time+datetime.timedelta(minutes=+duration)
    except Exception as e:
        unfreeze_time=datetime.datetime.now()

    result=setFreezeNum(account_id,user_id,freeze_num,club_id,operator_id,game_no,note,unfreeze_time)
    return HttpResponse(result)


def freeze_minilist(request):
    game_no=request.POST['game_no']
    tb_result=getFreezeListByGameNo(game_no)
    return render(request,'freeze_minilist.html', {'tb_result': tb_result})


def abortgame(request):
    operator_info = request.session['operator_info']
    operator_id = operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission = getPermission(operator_id)
    if not permission.filter(type_id=7).exists():
        return HttpResponseRedirect('/warning/')
    gameno=request.POST['game_no']
    result = abortGameByNo(gameno)
    return HttpResponse(result)


def union_account(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission = getPermission(operator_id)
    if not permission.filter(type_id=4).exists():
        return HttpResponseRedirect('/warning/')
    club_id = operator_info['club_id']
    group_id=operator_info['group_id']
    tb_result=getClubListWithoutSelf(club_id)
    tb_account_list=ucs_club_account.objects.filter(inactive_time='2037-01-01')\
        .filter(group_id=group_id).filter(club_id=club_id).values('account_id','account_desc')
    tb_union_balance=getUnionClubAccountList(club_id)
    return render(request, 'union_account.html', {'tb_club': tb_result,'tb_account': tb_account_list, 'tb_union_balance':tb_union_balance})


def union_account_list(request):
    club_id=request.POST['club_id']
    operator_info = request.session['operator_info']
    own_club_id = operator_info['club_id']
    tb_balance_list=getUnionBalanceList(club_id,own_club_id)
    return render(request, 'union_account_list.html',{'tb_balance_list': tb_balance_list})

def club_account_view(request):
    account_id=request.POST['account_id']
    club_name = request.POST['club_name']
    if account_id==0:
        return render(request, 'club_account_list.html')
    operator_info = request.session['operator_info']
    own_club_id = operator_info['club_id']
    tb_balance_list=getUnionBalanceList(own_club_id,account_id)
    return render(request, 'club_account_list.html',{'tb_balance_list': tb_balance_list, 'club_name': club_name})


def club_cash(request):
    operator_info = request.session['operator_info']
    group_id = operator_info['group_id']
    own_club_id=operator_info['club_id']
    operator_id=operator_info['operator_id']
    account_id=request.POST['account_id'] #本俱乐部财务账户ID
    op_type=request.POST['cash_type']
    club_id=request.POST['club_id']
    cash_num=request.POST['cash_num']
    chance=int(float(cash_num)*1000)
    note=request.POST['note']
    if op_type=='false':
        type_id=1004 #俱乐部充值
    elif op_type=='true':
        type_id=2002
        subs_account_id = ucs_union_account.objects.filter(inactive_time='2037-01-01').get(club_id=club_id).account_id
        balance=ucs_union_balance.objects.filter(inactive_time='2037-01-01').filter(account_id=subs_account_id)\
            .filter(main_club_id=own_club_id).order_by('-update_time')[0].balance
        #if (balance - chance)<0:
        #    result2=False
        #    return HttpResponse(result2)
        #else:
        try:
            balance=ucs_club_balance.objects.filter(inactive_time='2037-01-01').filter(account_id=account_id)\
                .order_by('-update_time')[0].balance
        except:
            balance=0
        if balance-chance<0:
            result2 = False
            return HttpResponse(result2)
    serialno=createSerialNo(own_club_id,group_id, type_id)
    result=operator_cash(account_id, chance, type_id, operator_id, note, serialno, group_id)
    if result:
        result_2=club_cash_func(operator_id,group_id,club_id,chance, type_id, serialno, note, own_club_id)
        return HttpResponse(result_2)
    else:
        result_2=False
        return HttpResponse(result_2)

#俱乐部账目核对
def union_check(request):
    operator_info = request.session['operator_info']
    operator_id = operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission = getPermission(operator_id)
    if not permission.filter(type_id=4).exists():
        return HttpResponseRedirect('/warning/')
    club_id=operator_info['club_id']
    club_level=operator_info['club_level']
    account_balance=getClubAccountTotal(club_id)
    user_balance=getClubBalanceTotal(club_id)
    union_balance=getUnionBalanceTotal(club_id, club_level)
    club_income=getClubIncomeTotal(club_id, club_level)
    deposit_sum = getDepoistSumByClub(club_id)
    up_total=getUnionIncomeTotal(club_id)
    income_total=(club_income+up_total)
    company=getCompanyBalanceSum(club_id)
    companySum=company[2]
    check=round((account_balance+deposit_sum-(user_balance+union_balance+club_income+up_total+companySum)),2)
    tb1={}
    tb1['account_balance']=round((account_balance+deposit_sum)/1000,2)
    tb1['user_balance'] = round(user_balance/1000,2)
    tb1['union_balance'] = round(union_balance/1000,2)
    tb1['club_income'] = round(club_income/1000,2)
    tb1['up_total'] = round(up_total/1000,2)
    tb1['income_total'] = round(income_total/1000,2)
    tb1['companysum']=round(companySum/1000,2)
    tb1['check'] = check
    usertype=getClubUserBalanceByType(club_id)
    clubtype=getUnionBalanceByType(club_id)
    tb2=round((usertype['userplus']+usertype['userminus']+clubtype['clubplus']+clubtype['clubminus']),2)
    tb_income=getClubIncomeByType(club_id, club_level)
    tb3={}
    tb3['total']=round((tb_income['total']+tb_income['up_total']),2)
    tb3['water']=round((tb_income['water']+tb_income['up_water']),2)
    tb3['insure']=round((tb_income['insure']+tb_income['up_insure']),2)
    tb4=getClubAccountBalanceByType(club_id)
    deposit_list=getDepositSumByType(club_id)
    tb4=list(tb4)
    for t in deposit_list:
        tb4.append(('提现中',t[0],t[1]))
    tb4_sum=0
    for t in tb4:
        tb4_sum=tb4_sum+t[2]
    return render(request, 'union_check.html', {'tb1':tb1,'usertype': usertype,'clubtype': clubtype,
                                                'tb2':tb2, 'tb_income':tb_income, 'tb3':tb3 , 'tb4':tb4,
                                                'tb4_sum': tb4_sum})


def group_balance_list(request):
    account_id=request.POST['account_id']
    tb_result= getClubBalanceByGroup(account_id)
    return render(request, 'group_balance_list_tb.html', {'tb_result': tb_result})

def group_balance_search(request):
    operator_info = request.session['operator_info']
    club_id=operator_info['club_id']
    group_id = operator_info['group_id']
    group_name=operator_info['group_name']
    group_list=[(group_id, group_name)]
    account_list=club_account_list(club_id, group_id)
    return render(request, 'group_balance_list.html', {'account_list': account_list,'group_list':group_list})


def company_account(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission = getPermission(operator_id)
    if not permission.filter(type_id=6).exists():
        return HttpResponseRedirect('/warning/')
    club_id=operator_info['club_id']
    group_list=ucs_operator_group.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id).values()
    type_list= pm_company_type.objects.filter(inactive_time='2037-01-01').order_by('type').values()
    return render(request,'company_account.html', {'group_list': group_list, 'type_list': type_list})


def getGroupAccount(request):
    operator_info = request.session['operator_info']
    club_id=operator_info['club_id']
    group_id=request.POST['group_id']
    tmp=getGroupAccountFunc(club_id,group_id)
    tb_account_list = json.dumps(tmp, cls=django.core.serializers.json.DjangoJSONEncoder)
    return HttpResponse(tb_account_list)


def company_cash(request):
    operator_info = request.session['operator_info']
    club_id=operator_info['club_id']
    group_id=operator_info['group_id']
    operator_id=operator_info['operator_id']
    account_id=request.POST['account_id']
    cash=request.POST['cash_num']
    note = request.POST['note']
    op_type_id=int(request.POST['op_type_id'])
    if op_type_id>2000 :
        type_id=2003
    else:
        type_id=1005

    serial_no = createSerialNo (club_id, group_id, type_id)

    cash_num=int(float(cash)*1000)
    if operator_cash(account_id,cash_num,type_id,operator_id,note, serial_no,group_id):

        companyCashFunc(club_id, account_id, cash_num, op_type_id, operator_id,serial_no, note)
        result=True
        return HttpResponse(result)

    else:
        result = False
        return HttpResponse(result)


def company_balance_list(request):
    operator_info = request.session['operator_info']
    club_id=operator_info['club_id']
    tb_list=getCompanyBalanceList(club_id)
    tb_total=getCompanyBalanceSum(club_id)
    tb_total_list=[]
    for t in tb_total:
        tb_total_list.append(round(t/1000,2))
    return render(request, 'company_account_tb.html',{'tb_list': tb_list,'tb_total': tb_total_list})


def getGameStatus(request):
    game_no=request.POST['game_no']
    try:
        status=ucs_gamerecord.objects.filter(inactive_time='2037-01-01').get(game_no=game_no).status_id
        if status<4:
            result=True
            return HttpResponse(result)
        else:
            result=False
            return HttpResponse(result)
    except:
        result=False
        return HttpResponse(result)


def correct_manage(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission = getPermission(operator_id)
    if not permission.filter(type_id=3).exists():
        return HttpResponseRedirect('/warning/')
    operator_info = request.session['operator_info']
    operator_id=operator_info['operator_id']
    operator_name = operator_info['operator_name']
    op_list=[(operator_id, operator_name)]
    return render(request,'correct_manage.html',{'op_list': op_list})


def correct_user_list(request):
    operator_id=request.POST['operator_id']
    operator_info = request.session['operator_info']
    club_id=operator_info['club_id']
    tb_result=getCorrectUserList(club_id, operator_id)
    return render(request, 'correct_user_list.html',{'tb_result': tb_result})


def correct_user(request):
    operator_info = request.session['operator_info']
    operator_id=operator_info['operator_id']
    group_id = operator_info['group_id']
    club_id=operator_info['club_id']
    serial_no=request.POST['serial_no']
    note = request.POST['note']
    new_serial_no=createSerialNo(club_id, group_id, 1002)
    result=correctUserFunc(serial_no, new_serial_no, note, operator_id)
    if result:
        result2=correctBalanceFunc(serial_no, new_serial_no, note, operator_id, group_id)
        return HttpResponse(result2)


def correct_club_list(request):
    operator_id=request.POST['operator_id']
    operator_info = request.session['operator_info']
    club_id=operator_info['club_id']
    tb_result=getCorrectClubList(club_id, operator_id)
    return render(request, 'correct_club_list.html', {'tb_result': tb_result})


def correct_club(request):
    operator_info = request.session['operator_info']
    operator_id=operator_info['operator_id']
    group_id = operator_info['group_id']
    club_id=operator_info['club_id']
    serial_no=request.POST['serial_no']
    note = request.POST['note']
    new_serial_no=createSerialNo(club_id, group_id, 1002)
    result=correctClubFunc(serial_no, new_serial_no, note, operator_id, club_id, group_id)
    if result:
        result2 = correctBalanceFunc(serial_no, new_serial_no, note, operator_id, group_id)
        return HttpResponse(result2)


def correct_company_list(request):
    operator_id=request.POST['operator_id']
    operator_info = request.session['operator_info']
    club_id=operator_info['club_id']
    tb_result=getCorrectCompanyList(club_id, operator_id)
    return render(request, 'correct_company_list.html',{'tb_result': tb_result})


def correct_company(request):
    operator_info = request.session['operator_info']
    operator_id=operator_info['operator_id']
    group_id = operator_info['group_id']
    club_id=operator_info['club_id']
    serial_no=request.POST['serial_no']
    note = request.POST['note']
    new_serial_no=createSerialNo(club_id, group_id, 1002)
    result=correctBalanceFunc(serial_no, new_serial_no, note, operator_id, group_id)
    if result:
        result2 = correctCompanyFunc(serial_no, new_serial_no, note, operator_id)
        return HttpResponse(result2)
    else:
        return HttpResponse(result)


def company_income_manage(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission = getPermission(operator_id)
    if not permission.filter(type_id=10).exists():
        return HttpResponseRedirect('/warning/')
    club_id = operator_info['club_id']
    club_level=operator_info['club_level']
    year=time.strftime("%Y", time.localtime())
    month=time.strftime("%Y%m", time.localtime())
    last_mothly=time.localtime()[1]-1 or 12
    last_moth=str(year)+str(last_mothly)
    month_list=(last_moth, month)
    income_list=getClubIncomeByType(club_id, club_level)
    return render(request, 'company_income_reg.html', {'month_list': month_list, 'income_list': income_list})


def company_income_reg(request):
    operator_info = request.session['operator_info']
    operator_id = operator_info['operator_id']
    club_id = operator_info['club_id']
    reg_month=request.POST['reg_month']
    flag=companyIncomeGameReg(club_id, reg_month)
    if flag:
        result=companyIncomeRegAccount(club_id, reg_month,operator_id)
        return HttpResponse(result)


def developer_manage(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission = getPermission(operator_id)
    if not permission.filter(type_id=8).exists():
        return HttpResponseRedirect('/warning/')
    return render(request, 'developer_manage.html')


def developer_new(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    club_list=ucs_subs_club.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id).values('income_rate','insure_rate')

    return render(request,'developer_new.html', {'club_list': club_list})


def check_developer(request):
    developer_name=request.POST['developer_name']
    try:
        ucs_developer.objects.filter(inactive_time='2037-01-01').get(developer_name=developer_name)
        result=False
        return HttpResponse(result)
    except:
        result=True
        return HttpResponse(result)


def developer_reg(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    developer_name=request.POST['developer_name']
    developer_desc=request.POST['note']
    income_rate=request.POST['income_rate']
    insure_rate=request.POST['insure_rate']
    result=developerRegFunc(club_id, developer_name, income_rate, insure_rate, developer_desc)
    return HttpResponse(result)


def developer_list(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    tb_list=getDeveloperListByClubID(club_id)
    return render(request, 'developer_list.html', {'tb_list': tb_list})


def developer_modify(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    tb=ucs_developer.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)\
                .values('developer_id', 'developer_name')
    club_list = ucs_subs_club.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id).values('income_rate',
                                                                                                        'insure_rate')
    return render(request, 'developer_modify.html', {'tb_list': tb,'club_list': club_list})


def developer_info(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    developer_id=request.POST['developer_id']
    tb=ucs_developer.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)\
                .filter(developer_id=developer_id).values('income_rate', 'insure_rate', 'developer_desc')
    tmp={}
    for t in tb:
        tmp['income_rate']=t['income_rate']
        tmp['insure_rate']=t['insure_rate']
        tmp['developer_desc']=t['developer_desc']
    result=json.dumps(tmp)
    return HttpResponse(result)


def developer_user(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    tb_developer=ucs_developer.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)\
                .values('developer_id', 'developer_name')
    tb_user=getUserListWithoutBand(club_id)
    return render(request,'developer_user.html',{'tb_developer':tb_developer, 'tb_user': tb_user})


def developer_user_reg(request):
    operator_info = request.session['operator_info']
    developer_id=request.POST['developer_id']
    user_id=request.POST['user_id']
    club_id = operator_info['club_id']
    result=UserDeveloperReg(developer_id, user_id, club_id)
    return HttpResponse(result)


def developer_user_list(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    developer_id = request.POST['developer_id']
    tb_user=getDeveUserList(club_id,developer_id)
    return render(request, 'developer_user_list.html',{'tb_user': tb_user})


def developer_user_club_list(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    tb_list=getDeveUserListByClub(club_id)
    return render(request,'developer_user_club.html',{'tb_list':tb_list})


def developer_unband(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    developer_id=request.POST['developer_id']
    user_id=request.POST['user_id']
    result=developerUserUnband(club_id, developer_id, user_id)

    return HttpResponse(result)


def app_initialize(request):
    supper = request.session['supper']
    if supper == 'paddy':
        return render(request,'manage/app_initialize.html')
    else:
        return HttpResponse("请重新登录")

def app_union_setup(request):
    club_name=request.POST['club_name']
    club_shortname=request.POST['club_shortname']
    try:
        if ucs_subs_club.objects.filter(inactive_time='2037-01-01').filter(club_id=1000).exists():
            return HttpResponse("False")
        t=ucs_subs_club(club_id=1000,
                        club_name=club_name,
                        club_shortname=club_shortname,
                        club_desc="",
                        income_rate=100,
                        insure_rate=100,
                        club_lever=0)
        t.save()
        t=ucs_union_account(account_id=4000,
                            club_id=1000)
        t.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")



def load_main_club(request):
    try:
        tb_list=ucs_subs_club.objects.filter(inactive_time='2037-01-01').get(club_id=1000)
        club_name=tb_list.club_name
        club_shortname=tb_list.club_shortname
        return render(request, 'manage/app_union_setup.html',{'club_name':club_name,'club_shortname':club_shortname})
    except:
        return render(request, 'manage/app_union_setup.html')



def test(request):

    return render(request,'test01.html')

def test02(request):
    return render(request, 'test02.html')


def app_operator(request):
    supper=request.session['supper']
    if supper=='paddy':
        tb_club=ucs_subs_club.objects.filter(inactive_time='2037-01-01').values('club_id', 'club_name')
        tb_permission=ucs_permission_group.objects.filter(inactive_time='2037-01-01').values('group_id','group_name')
        return render(request,'manage/app_operator.html',{'tb_club': tb_club,'tb_permission':tb_permission})
    else:
        return HttpResponse("请重新登录")


def app_operator_reg(request):
    operator_name=request.POST['operator_name']
    login_id=request.POST['login_id']
    club_id=request.POST['club_id']
    permission_group_id=request.POST['permission_group_id']
    result=add_operator_func(operator_name, login_id,club_id,permission_group_id)
    return HttpResponse(result)


def result_list_view(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if not permission.filter(type_id=4).exists():
        return HttpResponseRedirect('/warning/')

    return render(request, 'result_list_view.html')


def result_list(request):
    start_date=request.POST['start']
    end_date=request.POST['end']
    tb_result=getResultList(start_date, end_date)
    return render(request, 'result_list.html',{'tb_result': tb_result})


def developer_table_view(request):
    operator_info = request.session['operator_info']
    operator_id = operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission = getPermission(operator_id)
    if not permission.filter(type_id=11).exists():
        return HttpResponseRedirect('/warning/')
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    developer_list=ucs_developer.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id).values('developer_id', 'developer_name')

    return render(request, 'developer_table_view.html', {'developer_list': developer_list})


def developer_table_list(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    developer_id = request.POST['developer_id']
    start_date=request.POST['start_date']
    end_date=request.POST['end_date']
    tb_list=getDeveTableList(club_id, developer_id, start_date,end_date)
    return render(request, 'developer_table_list.html',{'tb_list' :tb_list})


def developer_table_detail(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    developer_id=request.POST['developer_id']
    game_no=request.POST['game_no']
    tb_result=getDeveTableDetail(club_id, game_no, developer_id)
    return render(request, 'developer_table_detail.html', {'tb_result': tb_result})


def report_developer(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if not permission.filter(type_id=11).exists():
        return HttpResponseRedirect('/warning/')
    return render(request, 'report/report_developer.html')


def report_developer_result(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    start_date=request.POST['start_date']
    end_date=request.POST['end_date']
    tb_result=getDeveResultByDate(club_id, start_date, end_date)
    tb_result_sum=getDeveResultSumBydate(club_id,start_date,end_date)
    return render(request,'report/report_developer_sum.html',{'tb_result': tb_result, 'starttime': start_date, 'endtime': end_date,'tb_result_sum':tb_result_sum})


def reward_manage(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    permission = getPermission(operator_id)
    if not permission.filter(type_id=5).exists():
        return HttpResponseRedirect('/warning/')
    return render(request, 'manage/configure_manage.html')


def reward_normal(request):
    tb_blind=pm_blind.objects.values('blind_id', 'blind_desc')
    tb_reward=pm_reward.objects.values('type_id','type_name')
    return render(request, 'manage/game_reward_normal.html', {'tb_blind': tb_blind,'tb_reward':tb_reward})


def reward_normal_add(request):
    blind_id=request.POST['blind_id']
    type_id=request.POST['type_id']
    reward=request.POST['reward']
    reward_input=int(float(reward)*1000)
    result=reward_normal_add_func(blind_id, type_id, reward_input)
    return HttpResponse(result)


def reward_normal_list(request):
    tb_result=getRewardNormalList()

    return render(request,'manage/game_normal_list.html',{'tb_result': tb_result})


def reward_normal_modify(request):
    blind_id=request.POST['blind_id']
    type_id=request.POST['type_id']
    reward=request.POST['reward']
    reward_input = int(float(reward) * 1000)
    result=rewardNormalModify(blind_id,type_id,reward_input)
    return HttpResponse(result)


def reward_normal_delete(request):
    blind_id=request.POST['blind_id']
    type_id=request.POST['type_id']
    result=rewardNormalDelete(blind_id, type_id)
    return HttpResponse(result)


def reward_normal_form(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    group_id = operator_info['group_id']
    game_no=request.POST['game_no']
    try:
        status_id=ucs_gamerecord.objects.filter(inactive_time='2037-01-01').get(game_no=game_no).status_id
        if (status_id==4 or status_id==5):
            return HttpResponse('False')
    except:
        return HttpResponse('False')

    reward_list=getRewardByGameno(game_no)
    tb_user=getRewardFromUserList(game_no, club_id)
    account_list=getGroupAccountList(club_id,group_id)
    tb_result={}
    tb_result['user_list']=tb_user
    tb_result['tb_reward']=reward_list
    tb_result['account_list']=account_list
    #result=json.dumps(tb_user, cls=django.core.serializers.json.DjangoJSONEncoder)
    result=json.dumps(tb_result)
    return HttpResponse(result)


def reward_normal_reg(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    group_id = operator_info['group_id']
    operator_id=operator_info['operator_id']
    t_reward=request.POST['reward']
    user_flag=request.POST['user_flag']
    user_account_id=request.POST['user_account_id']
    user_id=request.POST['user_id']
    reward=int(float(t_reward)*1000)
    op_account_id=request.POST['op_account_id']
    serial_no=createSerialNo(club_id,group_id,2004)
    if operator_cash(op_account_id, reward, 2004,operator_id, '牌局奖励', serial_no, group_id):
        #serial_no = createSerialNo(club_id, group_id, 2008)
        result=companyCashFunc(club_id, op_account_id, reward, 2008, operator_id, serial_no, '牌局奖励')
        if user_flag=='true':
            serial_no = createSerialNo(club_id, group_id, 1001)
            if userCashReg(user_account_id,user_id, club_id, 1001, operator_id, reward, '牌局奖励', serial_no):
                result=operator_cash(op_account_id, reward, 1001, operator_id, '牌局奖励', serial_no, group_id)
            return HttpResponse(result)
    else:
        result=False
    return HttpResponse(result)


def deposit_rate(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission = getPermission(operator_id)
    if not permission.filter(type_id=5).exists():
        return HttpResponseRedirect('/warning/')
    club_id = operator_info['club_id']
    group_id = operator_info['group_id']
    tb_list=pm_account_type.objects.filter(inactive_time='2037-01-01').values('type_id','type')

    return render(request, 'manage/deposit_rate.html', {'tb_list': tb_list})


def deposit_rate_reg(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    type_id=request.POST['type_id']
    rate=request.POST['rate']
    result=depositRateReg(club_id,type_id,rate)
    return HttpResponse(result)


def depoist_rate_list(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    tb_deposit=getDepositList(club_id)
    return render(request, 'manage/deposit_rate_list.html', {'tb_depoist': tb_deposit})


def depoist_rete_delete(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    type_id=request.POST['type_id']
    try:
        pm_deposit_rate.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id).filter(account_type=type_id).update(inactive_time=now())
        result=True
        return HttpResponse(result)
    except:
        result = False
        return HttpResponse(result)


def deposit(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission = getPermission(operator_id)
    if not permission.filter(type_id=1).exists():
        return HttpResponseRedirect('/warning/')
    club_id = operator_info['club_id']
    group_id=operator_info['group_id']
    group_name=operator_info['group_name']
    tb_account_list=get_club_account_infoByGroup(club_id, group_id)
    tb_account=getDepositAccountList(club_id,group_id)
    tb_account_target=ucs_club_account.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)\
                .filter(group_id=group_id).filter(type_id=3).values('account_id', 'account_desc')
    return render(request,'deposit.html', {'tb_account_list': tb_account_list, 'group_name':group_name, 'tb_account':tb_account, 'tb_account_target':tb_account_target})


def get_deposit_rate(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    type_id=request.POST['type_id']
    try:
        rate=pm_deposit_rate.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id).get(account_type=type_id).rate
        return HttpResponse(rate)
    except:
        return HttpResponse("False")


def deposit_reg(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    group_id=operator_info['group_id']
    operator_id=operator_info['operator_id']
    deposit=request.POST['deposit']
    deposit_input=int(deposit)*1000
    fee=request.POST['fee']
    fee_input=int(fee)*1000
    chance=deposit_input+fee_input
    account_id = request.POST['account_id']
    account_target_id = request.POST['account_target_id']
    type_id=request.POST['type_id']
    serial_no=createSerialNo(club_id,group_id, 2005)
    balance=getClubBalanceByAccount(account_id)
    if (int(balance)-(int(deposit_input)+int(fee_input)))>=0:
        if depositReg(serial_no, club_id, group_id, account_id, type_id, deposit_input, fee_input, operator_id,account_target_id):
            if operator_cash(account_id, chance, 2005, operator_id, '提现', serial_no, group_id):
                result=companyCashFunc(club_id, account_id, fee_input, 2009, operator_id, serial_no, '提现')
                return HttpResponse(result)
            else:
                return HttpResponse('False')
        else:
            return HttpResponse('False')
    else:
        return HttpResponse('False')


def deposit_list(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    group_id=operator_info['group_id']
    tb_result=getDepositBalanceList(club_id,group_id)
    return render(request,'depoist_list.html', {'tb_result':tb_result})


def deposit_arrived(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    group_id=operator_info['group_id']
    operator_id=operator_info['operator_id']
    serial_no=request.POST['serial_no']
    deposit=request.POST['deposit']
    account_target_id=request.POST['account_target_id']
    deposit_input=int(float(deposit)*1000)
    new_serial_no=createSerialNo(club_id, group_id,1007)
    if depositArrived(serial_no,operator_id,club_id, new_serial_no):
        result=operator_cash(account_target_id, deposit_input,1007, operator_id, '提现到账', new_serial_no, group_id)
        return HttpResponse(result)
    else:
        return HttpResponse('False')



def manage_account_setup(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    tb_group=ucs_operator_group.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id).values('group_id','group_name')
    tb_type=pm_account_type.objects.filter(inactive_time='2037-01-01').values('type_id', 'type')
    return render(request,'manage/account_setup.html',{'tb_group': tb_group, 'tb_type': tb_type})


def manage_account_type_list(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    tb_list=getGroupAccountFullList(club_id)
    return render(request, 'manage/account_type_list.html',{'tb_list': tb_list})


def manage_account_reg(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    group_id=request.POST['group_id']
    type_id=request.POST['type_id']
    account_desc=request.POST['account_desc']
    account_id=create_club_accountID(club_id)
    result=create_club_account(account_id, club_id,type_id, group_id,account_desc)
    return HttpResponse(result)


def manage_account_modify(request):
    account_id=request.POST['account_id']
    account_desc=request.POST['account_desc']
    result=modifyAccountDesc(account_id, account_desc)
    return HttpResponse(result)


def user_detail(request):
    try:
        operator_info = request.session['operator_info']
    except:
        return HttpResponseRedirect('/default/')
    operator_id = operator_info['operator_id']
    if operator_info['is_active']==False:
        return HttpResponseRedirect('/operator_disable/')
    permission = getPermission(operator_id)
    if not permission.filter(type_id=4).exists():
        return HttpResponseRedirect('/warning/')
    club_id = operator_info['club_id']
    tb_user=getUserListByClubId(club_id)
    return render(request,'user_detail.html', {'tb_user': tb_user})


def user_balance_full_list(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    account_id=request.POST['account_id']
    startdate=request.POST['startdate']
    enddate=request.POST['enddate']
    tb_balance=getUserBalanceListByDate(club_id,account_id, startdate,enddate)
    return render(request,'user_balance_full_list.html',{'tb_balance': tb_balance})


def user_result_full_list(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    user_id=request.POST['user_id']
    startdate=request.POST['startdate']
    enddate=request.POST['enddate']
    tb_result=getUserResultListByDate(club_id, user_id, startdate,enddate)
    return render(request, 'user_result_full_list.html', {'tb_result': tb_result})


def user_freeze_full_list(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    user_id=request.POST['user_id']
    startdate=request.POST['startdate']
    enddate=request.POST['enddate']
    tb_result=getUserFreezeListByDate(club_id, user_id, startdate,enddate)
    return render(request,'user_freeze_full_list.html',{'tb_result': tb_result})


def user_income_full_list(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    user_id=request.POST['user_id']
    startdate=request.POST['startdate']
    enddate=request.POST['enddate']
    tb_result=getUserIncomeListByDate(club_id, user_id, startdate,enddate)
    return render(request, 'user_income_full_list.html', {'tb_result': tb_result})


def warning(request):

    return render(request,'warning.html')


def permission(request):

    return render(request,'manage/permission.html')


def permission_group(request):
    try:
        tb_group=ucs_permission_group.objects.filter(inactive_time='2037-01-01').values('group_id', 'group_name')
        tb_permission=pm_permission.objects.filter(inactive_time='2037-01-01').values('type_id','permission')
    except:
        return HttpResponse('出错了')
    return render(request,'manage/permission_group.html',{'tb_group': tb_group,'tb_permission': tb_permission})


def get_permission_list(request):
    group_id=request.POST['group_id']
    try:
        #tb_permission = ucs_permission.objects.filter(inactive_time='2037-01-01').filter(group_id=group_id).values('type_id')
        tmp=getPermissionList(group_id)
        tb_list=json.dumps(tmp, cls=django.core.serializers.json.DjangoJSONEncoder)
        return HttpResponse(tb_list)
    except:
        return HttpResponse('False')

def permission_group_set(request):
    type_list=request.POST.getlist('type_list')
    group_id=request.POST['group_id']
    result=setPermissionGroup(group_id,type_list)
    return HttpResponse(result)


def permission_operator(request):
    try:
        tb_operator=ucs_operator.objects.filter(inactive_time='2037-01-01').values('operator_id','operator_name','login_id')
        tb_group=ucs_permission_group.objects.filter(inactive_time='2037-01-01').values('group_id','group_name')
        return render(request,'manage/permission_operator.html', {'tb_operator':tb_operator, 'tb_group': tb_group})
    except:
        return HttpResponse("出错了")


def permission_operator_list(request):
    tb_result=getPermissionOperatorList()

    return render(request,'manage/permission_operator_list.html',{'tb_result': tb_result})


def operator_set_active(request):
    is_active=request.POST['is_active']
    operator_id=request.POST['operator_id']
    if is_active=="启用":
        flag=True
    else:flag=False
    try:
        ucs_operator.objects.filter(inactive_time='2037-01-01').filter(operator_id=operator_id).update(is_active=flag)
        return HttpResponse('True')
    except Exception as e :
        return HttpResponse('False')


def operator_disable(request):

    return render(request,'manage/operator_disable.html')


def change_password(request):
    operator_info = request.session['operator_info']
    operator_id=operator_info['operator_id']
    operator_name = operator_info['operator_name']
    try:
        login_id=ucs_operator.objects.filter(inactive_time='2037-01-01').get(operator_id=operator_id).login_id
    except:
        return HttpResponseRedirect('operator_disable')
    return render(request,'manage/change_password.html',{'operator_name':operator_name, 'login_id':login_id})


def new_password(request):
    operator_info = request.session['operator_info']
    operator_id = operator_info['operator_id']
    old_password=request.POST['old_password']
    new_password=request.POST['new_password']
    result=changeOperatrorPassword(operator_id, old_password,new_password)
    return HttpResponse(result)


def reset_password(request):
    try:
        tb_operator = ucs_operator.objects.filter(inactive_time='2037-01-01').values('operator_id', 'operator_name',
                                                                                     'login_id')

        return render(request,'manage/permission_password.html',{'tb_operator':tb_operator})
    except:
        return HttpResponse("出错了")


def set_password(request):
    operator_id=request.POST['operator_id']
    new_password=request.POST['new_password']
    result=setOperatorPassword(operator_id,new_password)
    return HttpResponse(result)


def upload_result_img(request):
    filetype=request.POST['type']
    strtype=filetype.split('/')
    type=strtype[1]
    game_no=request.POST['game_no']
    if request.method =='POST':
        file=request.FILES.get("file",None)
        if not file:
            return HttpResponse("no files for upload")
        filename=createUploadImgName(1)+"."+type
        destination=open(os.path.join("sdt/static/upload",filename),'wb+');
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        try:
            ucs_gamerecord.objects.filter(inactive_time='2037-01-01').filter(game_no=game_no).update(img_url=filename)
            return HttpResponse(filename)
        except:
            return HttpResponse("False")


def result_img_show(request):
    game_no=request.POST['game_no']
    try:
        filename=ucs_gamerecord.objects.filter(inactive_time='2037-01-01').get(game_no=game_no).img_url
        url=filename
        return HttpResponse(url)
    except:
        return HttpResponse("False")


def user_result_min_list(request):
    user_name=request.POST['user_name']
    operator_info = request.session['operator_info']
    club_id=operator_info['club_id']
    try:
        user_id=ucs_subs_user.objects.filter(inactive_time='2037-01-01').get(user_name=user_name).user_id
        account_id=ucs_account.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id).get(user_id=user_id).account_id
    except:
        return HttpResponse('False')
    tb_balance_list=getUserBalenceList(account_id,club_id)
    tb_result = getUserAccountInfo(account_id, club_id)
    return render(request,'user_result_min_list.html',{'tb_balance_list':tb_balance_list,'tb_result':tb_result,'user_name':user_name})

def credit_manage(request):


    return render(request,'credit_manage.html')


def load_credit_user_reg(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    tb_result=getUserListWithoutCredit(club_id)
    return render(request, 'credit_user_reg.html',{'tb_result':tb_result})


def load_credit_user_list(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    tb_result=getCreditUserList(club_id)
    return render(request,'credit_user_list.html',{'tb_result':tb_result})


def credit_user_reg(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    operator_id=operator_info['operator_id']
    account_id=request.POST['account_id']
    credit_num=request.POST['credit_num']
    credit_num_input=int(float(credit_num)*1000)
    note=request.POST['note']
    result=creditUserReg(account_id, club_id, credit_num_input, operator_id,note)
    return HttpResponse(result)


def credit_user_disable(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    account_id=request.POST['account_id']
    result=creditUserDisable(account_id,club_id)
    return HttpResponse(result)


def credit_user_modify(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    operator_id = operator_info['operator_id']
    account_id = request.POST['account_id']
    credit_num = request.POST['credit_num']
    credit_num_input = int(float(credit_num) * 1000)
    note = request.POST['note']
    if creditUserDisable(account_id,club_id):
        result=creditUserReg(account_id, club_id, credit_num_input, operator_id,note)
        return HttpResponse(result)
    else:
        return HttpResponse('False')


def load_credit_developer_reg(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    try:
        tb_list=ucs_developer.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)\
            .values('developer_id','developer_name')
    except:
        return HttpResponse('出错啦')
    return render(request,'credit_developer_reg.html',{'tb_list':tb_list})


def load_credit_developer_list(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    tb_result=getCreditDeveloperList(club_id)
    return render(request,'credit_developer_list.html',{'tb_result':tb_result})


def credit_developer_reg(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    operator_id = operator_info['operator_id']
    developer_id=request.POST['developer_id']
    credit_num = request.POST['credit_num']
    credit_num_input = int(float(credit_num) * 1000)
    note = request.POST['note']
    result=creditDeveloperReg(developer_id,club_id,credit_num_input,note,operator_id)
    return HttpResponse(result)


def credit_developer_disable(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    developer_id=request.POST['developer_id']
    result=creditDeveloperDisable(developer_id,club_id)
    return HttpResponse(result)


def credit_developer_modify(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    operator_id = operator_info['operator_id']
    developer_id=request.POST['developer_id']
    credit_num = request.POST['credit_num']
    credit_num_input = int(float(credit_num) * 1000)
    note = request.POST['note']
    if creditDeveloperDisable(developer_id,club_id):
        result=creditDeveloperReg(developer_id, club_id,credit_num_input,note,operator_id)
    return HttpResponse(result)
