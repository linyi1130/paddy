from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import render,HttpResponse
from django.template import Context,Template,RequestContext
from django.template import loader
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from sdt.models import *
from sdt.sdt_func import *
from .form import *
import datetime
import json
import django.core.serializers.json
from django.contrib import messages
from django.forms.models import model_to_dict
# Create your views here.
def club_list(request):
    t_club = getCLubList()
    return render(request, 'club.html', {'t_club': t_club})


def club_add(request):
    club_name=request.POST['club_name']
    club_shortname = request.POST['short_name']
    income_rate = request.POST['income_rate']
    club_desc = request.POST['club_desc']
    insure_rate = request.POST['insure_rate']
    result=club_reg(club_name, club_shortname,club_desc, income_rate, insure_rate )
    if result:
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
    user_name=request.POST['user_name']
    wx_name=request.POST['wx_name']
    note=request.POST['wx_name']
    club_id=request.POST['club_id']
    result=checkUserExist(user_name,club_id)
    if result==0:
        flag=user_reg(user_name, wx_name, club_id, note)

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
    operator_info = request.session['operator_info']
    club_id=operator_info['club_id']
    tb_club=ucs_subs_club.objects.filter(inactive_time='2037-01-01').filter(club_id=club_id)
    return render(request,'user.html',{'tb_club':tb_club})

def user_list(request):
    club_id=request.POST['club_id']
    tb_result=getUserListByClubId(club_id)
    return render(request, 'user_list.html',{'tb_user': tb_result})

def cash(request):
    operator_info=request.session['operator_info']
    operator_name=operator_info['operator_name']
    club_name=operator_info['club_name']
    club_id = operator_info['club_id']
    group_id = operator_info['group_id']
    group_name=operator_info['group_name']
    tb_user = SQL_user_list(club_id)
    tb_type_list=club_account_list(club_id,group_id)
    return render(request, 'cash.html', {'tb_user': tb_user,'operator_name':operator_name,
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
    ante=pm_ante.objects.filter(blind_id=1).order_by('id')
    return render(request, 'table.html', {'gametype':gametype,'blind':blind,"gametime":gametime,"gamepeople":gamepeople, "ante":ante})

def getante(request):
    blind_id=request.POST['blind_id']
    tmp=getAnteList(blind_id)
    ante_list = json.dumps(tmp, cls=django.core.serializers.json.DjangoJSONEncoder)
    return HttpResponse(ante_list)

def table_list(request):

    tb_result=getTableList()
    return render(request,'table_list.html', {'table_list': tb_result})


def game_reg(request):
    operator_info = request.session['operator_info']
    operator_id=operator_info['operator_id']
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
    t_club = getClubListMini()
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
    operator_info = request.session['operator_info']
    account_id=request.POST['account_id']
    user_id=request.POST['user_id']
    user_name=request.POST['user_name']
    club_id=operator_info['club_id']
    tb_result=getUserAccountInfo(account_id,club_id)
    tb_balance_list=getUserBalenceList(account_id,club_id)
    club_name=operator_info['club_name']
    tb_freeze=getFreezeListByUid(user_id)
    return render(request, 'user_account_info.html',{'user_name':user_name,'tb_result':tb_result,
                                                     'club_name':club_name,'tb_balance_list':tb_balance_list, 'tb_freeze':tb_freeze})

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
    operator_account_id = get_operator_accountID(club_id, group_id, type_id)
    if chang_type == "false":
        cashtype=1001  #客服充值
        serial_no = createSerialNo(club_id, group_id, type_id)
        result=userCashReg(account_id, user_id, club_id, cashtype, operator_id, change_num, note,serial_no)
        if result: #用户充值成功
            flag=operator_cash(operator_account_id, change_num, cashtype, operator_id, note,serial_no, group_id)
            if flag:
                tb_result = getUserAccountInfo(account_id, club_id)
                tb_balance_list = getUserBalenceList(account_id, club_id)
                return render(request, 'user_account_info.html', {'user_name': user_name, 'tb_result': tb_result,
                                                    'club_name':club_name, 'tb_balance_list': tb_balance_list})
            return HttpResponse("出错了")
        else: return HttpResponse("出错了")
    elif chang_type=='true':
        cashtype = 2001
        serial_no=createSerialNo(club_id, group_id,type_id)
        result = userCashReg(account_id, user_id, club_id, cashtype, operator_id, change_num, note, serial_no)
        if result:  # 用户充值成功
            flag = operator_cash(operator_account_id, change_num, cashtype, operator_id, note, serial_no)
            if flag:
                tb_result = getUserAccountInfo(account_id, club_id)
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
            serial_no=createSerialNo(club_id,1,1)
            if create_club_account(account_id,club_id,cnt,message):
                operator_cash(account_id, 0, 9999, 9999, "初始化",serial_no)
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


def club_account_info(request):
    operator_info=request.session['operator_info']
    club_id = operator_info['club_id']
    group_id = operator_info['group_id']
    tb_result=get_club_account_infoByGroup(club_id,group_id)
    return render(request, 'account_info.html', {'tb_result': tb_result})


def check_balance(request):
    operator_info = request.session['operator_info']
    account_id = request.POST['account_id']
    club_id = operator_info['club_id']
    group_id = operator_info['group_id']
    type_id = request.POST['pay_account']
    change_num = int(float(request.POST['change_num']) * 1000)
    operator_account_id = get_operator_accountID(club_id, group_id, type_id)
    user_balance = getBalancebyaid(account_id)
    if change_num>user_balance:
        msg=1
        return HttpResponse(msg)
    type_balance = get_club_balance_byType(operator_account_id)
    if change_num>type_balance:
        msg=2
        return HttpResponse(msg)
    msg=True
    return HttpResponse(msg)

def test(request):

    return render(request,'test01.html')

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
    club_id=operator_info['club_id']

    tb_user = getUserListByClubId(club_id)
    return render(request,'user_modify.html', {'tb_user':tb_user,'club_id': club_id})

def user_account_group(request):
    operator_info=request.session['operator_info']
    club_id=operator_info['club_id']

    tb_user = getUserListByClubId(club_id)
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
    return render(request, 'buyinregsubs.html',{'tb_user': tb_user, 'gameno': gameno})


def getusefulbalance(request):
    account_id=request.POST['account_id']
    balance=getBalancebyaid(account_id)
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
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
    gameno=request.POST['game_no']
    result = abortGameByNo(gameno)
    return HttpResponse(result)


def union_account(request):
    operator_info = request.session['operator_info']
    club_id = operator_info['club_id']
    group_id=operator_info['group_id']
    tb_result=getClubListWithoutSelf(club_id)
    tb_account_list=club_account_list(club_id,group_id)
    return render(request, 'union_account.html', {'tb_club': tb_result,'tb_account': tb_account_list})


def union_account_list(request):

    return render(request, 'union_account_list.html')

