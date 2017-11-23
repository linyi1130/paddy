from django.shortcuts import render,HttpResponsefrom django.template import Context,Templatefrom django.template import loaderfrom django.http import HttpResponseRedirectfrom sdt.models import *from django.db import connectionimport datetimedef user_reg(user_name,wx_name,club_id,t_note ): #注册新用户    t_real_user = real_user(user_name=user_name)    t_real_user.save()  # 生成了USERID    tmp = real_user.objects.filter(user_name=user_name)    t_user_id=tmp.order_by('-active_time')[0].user_id    t_account = real_account(user_id=t_user_id)    t_account.save()  # 生成了account_ID    t_tmp = real_account.objects.filter(user_id=t_user_id)    # 生成了ACCOUNTID    t_account_id = t_tmp.order_by('-active_time')[0].account_id    #t_club_id = ucs_subs_club.objects.get(club_name=club_name).club_id  # 取club_id    t_ucs_subs_user = ucs_subs_user(user_id=t_user_id,                                    account_id=t_account_id,                                    user_name=user_name,                                    wx_name=wx_name,                                    note=t_note                                    )    t_ucs_subs_user.save()  # 保存到usc_subs_user    t_ucs_account = ucs_account(user_id=t_user_id,                                account_id=t_account_id)    t_ucs_account.save()  # account_id 写入    t_club = ucs_club_user(user_id=t_user_id,                           club_id=club_id)    t_club.save()    return Truedef SQL_user_list():    with connection.cursor() as cursor :        strSQL="select b.user_id,b.account_id,b.user_name,b.wx_name,a.club_name,b.note "\        "from sdt_ucs_subs_club  a, sdt_ucs_subs_user  b, sdt_ucs_club_user c "\        "where a.club_id=c.club_id " \        "and c.user_id=b.user_id " \        "and date_format(b.inactive_time,'%Y')='2037' " \        "and date_format(a.inactive_time,'%Y')='2037' " \        "and date_format(c.inactive_time,'%Y')='2037' "\        "order by b.active_time desc"        cursor.execute(strSQL)        row = cursor.fetchall()    return rowdef getaccIDwithUserid(user_id):#用userid 获取accountid    try :        account_id = ucs_subs_user.objects.filter(inactive_time='2037-01-01').get(user_id=user_id).account_id    except Exception as e:        return e    return account_iddef getBalancebyaid(account_id):    try :        banlance=ucs_balance.objects.filter(account_id=account_id).order_by('-updatetime')[0].balance    except Exception as e:        return 0    return banlance,account_iddef getBalancebyuid(userid):    try :        account_id=ucs_subs_user.objects.filter(user_id=userid).get(inactive_time='2037-01-01').account_id        banlance=ucs_balance.objects.filter(account_id=account_id).order_by('-updatetime')[0].balance    except Exception as e:        return 0,account_id    return banlance,account_iddef getBalanceList(account_id):    with connection.cursor() as cursor:        strsql="select b.user_id,b.user_name,a.account_id,truncate(a.balance/1000,2) balance, "\        "truncate(a.chance/1000,2) chance,a.chance_desc,a.updatetime "\        "From sdt_ucs_balance a,sdt_ucs_subs_user b "\        "where date_format(a.inactive_time,'%%Y')='2037' "\        "and date_format(b.inactive_time,'%%Y')='2037' "\        "and a.account_id = b.account_id "\        "and a.account_id = %s "\        "order by a.updatetime desc"        cursor.execute(strsql,account_id)        row = cursor.fetchall()    return rowdef getante(blind):    ante=pm_ante.objects.filter(blind_id=blind)    return antedef createGameNo():    today=datetime.datetime.now().strftime('%Y-%m-%d')    part1 = datetime.datetime.now().strftime('%Y%m%d')    if ucs_gameno.objects.exists():        tmp=ucs_gameno.objects.all().order_by('-id')[0]        p=part1+"001"        if tmp.gametime.strftime('%Y-%m-%d')!=today:            #当天第一局            t=ucs_gameno(cnt=1,                        game_no=str(p))            t.save()            return p        else :            #当天局号继续生成            t1=int(tmp.game_no)+1            t=ucs_gameno(cnt=tmp.cnt+1,                         game_no=str(t1))            t.save()            return t1    else:        #空表        p2 = part1 + "001"        t = ucs_gameno(cnt=1,                       game_no=str(p2))        t.save()        return p2    return Nonedef result_preload(strResult):    p = str(strResult).replace(":", " ")  # 替换：为空格    # 按照空格拆分    list_insert = []    cnt = 8    t = p.split()    listlen = len(t)    while cnt < listlen:        list_insert.append(            tmp_result(user_name=p.split()[cnt], type=p.split()[cnt + 1], score=p.split()[cnt + 2]))  # 总带入        list_insert.append(            tmp_result(user_name=p.split()[cnt], type=p.split()[cnt + 3], score=p.split()[cnt + 4]))  # 保险收益        list_insert.append(            tmp_result(user_name=p.split()[cnt], type=p.split()[cnt + 5], score=p.split()[cnt + 6]))  # 牌局收益        list_insert.append(            tmp_result(user_name=p.split()[cnt], type=p.split()[cnt + 7], score=p.split()[cnt + 8]))  # 总收入        cnt = cnt + 9    tmp_result.objects.bulk_create(list_insert)    return Truedef result_reg(strResult,gameno):    strsql="delete from sdt_tmp_result_step_3 where game_no=%s "    #读取数据源并拆分数组    p = str(strResult).replace(":", " ")  # 替换：为空格    # 按照空格拆分    list_insert = []    cnt = 8    t = p.split()    listlen = len(t)    while cnt < listlen:        list_insert.append(            tmp_result(user_name=p.split()[cnt], type=p.split()[cnt + 1], score=p.split()[cnt + 2]))  # 总带入        list_insert.append(            tmp_result(user_name=p.split()[cnt], type=p.split()[cnt + 3], score=p.split()[cnt + 4]))  # 保险收益        list_insert.append(            tmp_result(user_name=p.split()[cnt], type=p.split()[cnt + 5], score=p.split()[cnt + 6]))  # 牌局收益        list_insert.append(            tmp_result(user_name=p.split()[cnt], type=p.split()[cnt + 7], score=p.split()[cnt + 8]))  # 总收入        cnt = cnt + 9    tmp_result.objects.bulk_create(list_insert)    #匹配俱乐部信息    with connection.cursor() as cursor:        strsql="insert into  sdt_tmp_result_step_1 (user_id,account_id,user_name, club_id, club_name,income_rate,insure_rate,game_no)"\            "select b.user_id,b.account_id,b.user_name,c.club_id,d.club_name,d.income_rate,d.insure_rate,%s from "\            "(select distinct user_name from sdt_tmp_result) as a, "\            "sdt_ucs_subs_user b, "\            "sdt_ucs_club_user c, "\            "sdt_ucs_subs_club d "\            "where a.user_name=b.user_name "\            "and b.user_id=c.user_id "\            "and c.club_id=d.club_id "\            "and date_format(b.inactive_time,'%%Y')='2037' "\            "and date_format(c.inactive_time,'%%Y')='2037' "\		    "and date_format(d.inactive_time,'%%Y')='2037' "        cursor.execute(strsql,gameno)        strsql="commit"        cursor.execute(strsql)        strsql="insert into sdt_tmp_result_step_2 (user_id,account_id,club_id,club_name,user_name,type,score,income_rate,income,game_no,score_final) "\            "select b.user_id,b.account_id,b.club_id,b.club_name,b.user_name,a.type,cast(a.score*1000 as signed),"\            "b.income_rate,cast(abs(a.score*b.income_rate/100*0.025)*1000 as signed) income , game_no, "\            "case when a.score>0 then a.score*0.95 else a.score end score_final "\            "from sdt_tmp_result a,sdt_tmp_result_step_1 b "\            "where a.user_name=b.user_name "\            "and a.type=\"总收益\" "\			"union all "\            "select b.user_id,b.account_id,b.club_id,b.club_name,b.user_name,a.type,cast(a.score*1000 as signed),"\            "b.income_rate,cast((a.score*b.insure_rate/100*-0.975)*1000 as signed) insure ,game_no, " \            "case when a.score>0 then a.score*0.95 else a.score end score_final " \            "from sdt_tmp_result a,sdt_tmp_result_step_1 b "\            "where a.user_name=b.user_name "\            "and a.type=\"保险收益\""        cursor.execute(strsql)        strsql="commit"        cursor.execute(strsql)        strsql="insert into sdt_tmp_result_step_3 (user_id,account_id,user_name,club_name,score,income_water,waterup,"\			"insure,income_insure,insure_up,income_total,up_total,delivery,game_no,score_final) "\            "select a.user_id,a.account_id, a.user_name,a.club_name,a.score ,a.income income_water, "\            "cast(abs(a.score)*0.025-a.income  as signed) waterup, "\            "b.score insure,b.income income_insure,cast((b.score*-0.975-b.income) as signed) insure_up,a.income+b.income income_total, "\            "cast((abs(a.score)*0.025-a.income+(b.score*-0.975-b.income)) as signed) up_total, "\			"cast((a.score*0.975+a.income+b.income) as signed) delivery,a.game_no,a.score_final "\            "from (select * from sdt_tmp_result_step_2 where type=\"总收益\") as a, "\            "(select * from sdt_tmp_result_step_2 where type=\"保险收益\") as b "\            "where a.user_id=b.user_id "        cursor.execute(strsql)        strsql="commit"        cursor.execute(strsql)        strsql="select user_name,club_name,round(income_water/1000,2) income_water, "\            "round(score/1000,2) score,round(waterup/1000,2) waterup,round(insure/1000,2) insure, "\            "round(income_insure/1000,2) income_insure,round(insure_up/1000,2) insure_up, "\            "round(income_total/1000,2) income_total,round(up_total/1000,2) up_total, "\            "round(delivery/1000,2) delivery "\            "from sdt_tmp_result_step_3 a "        cursor.execute(strsql)        try:            tb_result=cursor.fetchall()        except Exception as e:            return e    return tb_result