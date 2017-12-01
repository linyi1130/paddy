from sdt.models import *from django.db import connectionimport datetimedef user_reg(user_name,wx_name,club_id,t_note ): #注册新用户    if user_check(user_name)==False:        t_real_user = real_user(user_name=user_name)        t_real_user.save()  # 生成了USERID        tmp = real_user.objects.filter(user_name=user_name)        t_user_id=tmp.order_by('-active_time')[0].user_id        t_account = real_account(user_id=t_user_id)        t_account.save()  # 生成了account_ID        t_tmp = real_account.objects.filter(user_id=t_user_id)        # 生成了ACCOUNTID        t_account_id = t_tmp.order_by('-active_time')[0].account_id        #t_club_id = ucs_subs_club.objects.get(club_name=club_name).club_id  # 取club_id        t_ucs_subs_user = ucs_subs_user(user_id=t_user_id,                                        account_id=t_account_id,                                        user_name=user_name,                                        wx_name=wx_name,                                        note=t_note                                        )        t_ucs_subs_user.save()  # 保存到usc_subs_user        t_ucs_account = ucs_account(user_id=t_user_id,                                    account_id=t_account_id,                                    club_id=club_id)        t_ucs_account.save()  # account_id 写入        t_club = ucs_club_user(user_id=t_user_id,                               club_id=club_id)        t_club.save()    else: return False    return Truedef user_old_reg(user_id,club_id):    result=False    try:        tmp=ucs_club_user.objects.filter(inactive_time="2037-01-01").filter(user_id=user_id).filter(club_id=club_id)        if len(tmp)>0:            result=False        else:            t=ucs_club_user(club_id=club_id,                            user_id=user_id)            t.save()            result=True    except Exception as e:        result=False    return resultdef SQL_user_list():    with connection.cursor() as cursor :        strSQL="select b.user_id,b.account_id,b.user_name,b.wx_name,a.club_name,b.note,c.active_time "\        "from sdt_ucs_subs_club  a, sdt_ucs_subs_user  b, sdt_ucs_club_user c "\        "where a.club_id=c.club_id " \        "and c.user_id=b.user_id " \        "and date_format(b.inactive_time,'%Y')='2037' " \        "and date_format(a.inactive_time,'%Y')='2037' " \        "and date_format(c.inactive_time,'%Y')='2037' "\        "order by b.active_time desc"        cursor.execute(strSQL)        row = cursor.fetchall()    return rowdef getaccIDwithUserid(user_id):#用userid 获取accountid    try :        account_id = ucs_subs_user.objects.filter(inactive_time='2037-01-01').get(user_id=user_id).account_id    except Exception as e:        return e    return account_iddef getBalancebyaid(account_id):    try :        banlance=ucs_balance.objects.filter(account_id=account_id).order_by('-updatetime')[0].balance    except Exception as e:        return 0    return banlance,account_iddef getBalancebyuid(userid):    try :        account_id=ucs_subs_user.objects.filter(user_id=userid).get(inactive_time='2037-01-01').account_id        banlance=ucs_balance.objects.filter(account_id=account_id).order_by('-updatetime')[0].balance    except Exception as e:        return 0,account_id    return banlance,account_iddef getBalanceList(account_id):    with connection.cursor() as cursor:        strsql="select b.user_id,b.user_name,a.account_id,truncate(a.balance/1000,2) balance, "\        "truncate(a.chance/1000,2) chance,a.chance_desc,a.updatetime "\        "From sdt_ucs_balance a,sdt_ucs_subs_user b "\        "where date_format(a.inactive_time,'%%Y')='2037' "\        "and date_format(b.inactive_time,'%%Y')='2037' "\        "and a.account_id = b.account_id "\        "and a.account_id = %s "\        "order by a.updatetime desc"        cursor.execute(strsql,account_id)        row = cursor.fetchall()    return rowdef getante(blind):    ante=pm_ante.objects.filter(blind_id=blind)    return antedef createGameNo():    today=datetime.datetime.now().strftime('%Y-%m-%d')    part1 = datetime.datetime.now().strftime('%Y%m%d')    if ucs_gameno.objects.exists():        tmp=ucs_gameno.objects.all().order_by('-id')[0]        p=part1+"001"        if tmp.gametime.strftime('%Y-%m-%d')!=today:            #当天第一局            t=ucs_gameno(cnt=1,                        game_no=str(p))            t.save()            return p        else :            #当天局号继续生成            t1=int(tmp.game_no)+1            t=ucs_gameno(cnt=tmp.cnt+1,                         game_no=str(t1))            t.save()            return t1    else:        #空表        p2 = part1 + "001"        t = ucs_gameno(cnt=1,                       game_no=str(p2))        t.save()        return p2    return Nonedef result_preload(strResult,gameno):    tmp_result.objects.filter(game_no=gameno).delete()    p = str(strResult).replace(":", " ")  # 替换：为空格    # 按照空格拆分    list_insert = []    cnt = 8    t = p.split()    listlen = len(t)    while cnt < listlen:        list_insert.append(            tmp_result(user_name=p.split()[cnt], type=p.split()[cnt + 1], score=p.split()[cnt + 2],game_no=gameno))  # 总带入        list_insert.append(            tmp_result(user_name=p.split()[cnt], type=p.split()[cnt + 3], score=p.split()[cnt + 4],game_no=gameno))  # 保险收益        list_insert.append(            tmp_result(user_name=p.split()[cnt], type=p.split()[cnt + 5], score=p.split()[cnt + 6],game_no=gameno))  # 牌局收益        list_insert.append(            tmp_result(user_name=p.split()[cnt], type=p.split()[cnt + 7], score=p.split()[cnt + 8],game_no=gameno))  # 总收入        cnt = cnt + 9    tmp_result.objects.bulk_create(list_insert)    return True#筛选战绩中新玩家def result_regNewUser(gameno):    with connection.cursor() as cursor:        strSQL="select DISTINCT a.user_name from sdt_tmp_result a "\                "where a.game_no=%s "\                "and a.user_name not in "\                "(select b.user_name from sdt_ucs_subs_user b where date_format(b.inactive_time,'%%Y')='2037') "        cursor.execute(strSQL,gameno)        row = cursor.fetchall()    return rowdef result_attachclub(gameno):    userlist=[]    with connection.cursor() as cursor:        strSQL="select x.user_id,x.account_id,x.user_name,y.club_id,z.club_name,z.income_rate,z.insure_rate,x.game_no from ( "\               " select a.user_id,a.account_id,a.user_name,b.game_no,count(*) from sdt_ucs_subs_user a, "\               "(select distinct user_name,game_no from sdt_tmp_result) b, "\               "sdt_ucs_club_user c "\               "where a.user_name=b.user_name "\               "and date_format(a.inactive_time,'%%Y')='2037' "\               "and a.user_id=c.user_id "\               "and b.game_no=%s "\               "and date_format(c.inactive_time,'%%Y')='2037' "\               "group by a.user_id,a.account_id,a.user_name,b.game_no "\               "having count(*)>1) x, "\               "sdt_ucs_club_user y, "\               "sdt_ucs_subs_club z "\               "where x.user_id=y.user_id "\               "and date_format(y.inactive_time,'%%Y')='2037' "\               "and y.club_id=z.club_id "\               "and date_format(z.inactive_time,'%%Y')='2037' "\               "order by user_id asc "        cursor.execute(strSQL,gameno)        row = cursor.fetchall()        if len(row)>0:            sp_club=[]            tmp_id=row[0][0]            tmp_name=row[0][2]            for t in row:                if tmp_name == t[2]:                    sp_club.append((t[3], t[4]))                else:                    userlist.append((tmp_id,tmp_name, sp_club))                    sp_club = []                    tmp_name = t[2]                    tmp_id=t[0]                    sp_club.append((t[3], t[4]))            userlist.append((tmp_id, tmp_name, sp_club))            return userlist        else:            return userlistdef split_club(split_result={}):    tmp_club_user=[]    gameno=split_result['gameno']    tmp_result_attachclub_pre.objects.filter(gameno=gameno).delete()    if len(split_result) > 0:        for key in split_result:            if key != "gameno":                tmp_club_user.append(split_result[key])        lenlist=len(tmp_club_user)        i=0        tmp_result_attachclub_pre.objects.filter(gameno=gameno).delete()        while (i < lenlist):            t = tmp_result_attachclub_pre(gameno=gameno,                                    user_id=tmp_club_user[i],                                    user_name=tmp_club_user[i+1],                                    club_id=tmp_club_user[i+2])            t.save()            i=i+3        with connection.cursor() as cursor:            strSQL="insert into sdt_tmp_result_attachclub_pre (gameno,user_id,user_name,club_id) "\                   "select x.game_no,x.user_id,x.user_name,y.club_id from ( "\                   "select  b.game_no,a.user_id,a.user_name,count(*) from sdt_ucs_subs_user a, "\                   "(select distinct user_name,game_no from sdt_tmp_result) b, "\                   "sdt_ucs_club_user c "\                   "where a.user_name=b.user_name "\                   "and b.game_no=%s "\                   "and date_format(a.inactive_time,'%%Y')='2037' "\                   "and a.user_id=c.user_id "\                   "and date_format(c.inactive_time,'%%Y')='2037' "\                   "group by a.user_id,a.account_id,a.user_name,b.game_no "\                   "having count(*)=1) x, "\                   "sdt_ucs_club_user y, "\                   "sdt_ucs_subs_club z "\                   "where x.user_id=y.user_id "\                   "and date_format(y.inactive_time,'%%Y')='2037' "\                   "and y.club_id=z.club_id "\                   "and date_format(z.inactive_time,'%%Y')='2037' "\                   "order by user_id asc"            cursor.execute(strSQL, gameno)            strSQL="commit"            cursor.execute(strSQL)    else:        #没有需要手工分的俱乐部        with connection.cursor() as cursor:            strSQL="insert into sdt_tmp_result_attachclub_pre "\                   "select x.game_no,x.user_id,x.user_name,y.club_id from ( "\                   "select  b.game_no,a.user_id,a.user_name,count(*) from sdt_ucs_subs_user a, "\                   "(select distinct user_name,game_no from sdt_tmp_result) b, "\                   "sdt_ucs_club_user c "\                   "where a.user_name=b.user_name "\                   "and game_no=%s "\                   "and date_format(a.inactive_time,'%%Y')='2037' "\                   "and a.user_id=c.user_id "\                   "and date_format(c.inactive_time,'%%Y')='2037' "\                   "group by a.user_id,a.account_id,a.user_name,b.game_no "\                   "having count(*)=1) x, "\                   "sdt_ucs_club_user y, "\                   "sdt_ucs_subs_club z "\                   "where x.user_id=y.user_id "\                   "and date_format(y.inactive_time,'%%Y')='2037' "\                   "and y.club_id=z.club_id "\                   "and date_format(z.inactive_time,'%%Y')='2037' "\                   "order by user_id asc"            cursor.execute(strSQL, gameno)            strSQL="commit"            cursor.execute(strSQL)    return Truedef result_reg(gameno):    tmp_result_step_1.objects.filter(game_no=gameno).delete()    tmp_result_step_2.objects.filter(game_no=gameno).delete()    tmp_result_step_3.objects.filter(game_no=gameno).delete()    #匹配俱乐部信息    with connection.cursor() as cursor:        strsql="insert into sdt_tmp_result_step_1 (user_id,account_id,user_name, club_id, club_name,income_rate,insure_rate,game_no) "\               "select a.user_id,c.account_id,a.user_name,b.club_id,b.club_name,b.income_rate,b.insure_rate,a.gameno "\               "from sdt_tmp_result_attachclub_pre a, "\               "sdt_ucs_subs_club b, "\               "sdt_ucs_account c "\               "where a.club_id=b.club_id "\               "and date_format(b.inactive_time,'%%Y')='2037' "\               "and a.user_id=c.user_id "\               "and b.club_id=c.club_id "\               "and date_format(c.inactive_time,'%%Y')='2037' "\               "and a.gameno=%s"        cursor.execute(strsql, gameno)        strsql="commit"        cursor.execute(strsql)        strsql="insert into sdt_tmp_result_step_2 (user_id,account_id,club_id,club_name,user_name,type,score,income_rate,income,game_no,score_final) "\            "select b.user_id,b.account_id,b.club_id,b.club_name,b.user_name,a.type,cast(a.score*1000 as signed),"\            "b.income_rate,cast(abs(a.score*b.income_rate/100*0.025)*1000 as signed) income , b.game_no, "\            "case when a.score>0 then a.score*0.95*1000 else a.score*1000 end score_final "\            "from sdt_tmp_result a,sdt_tmp_result_step_1 b "\            "where a.user_name=b.user_name "\            "and a.type=\"总收益\" "\            "and a.game_no=b.game_no "\            "and a.game_no=%s "\			"union all "\            "select b.user_id,b.account_id,b.club_id,b.club_name,b.user_name,a.type,cast(a.score*1000 as signed),"\            "b.income_rate,cast((a.score*b.insure_rate/100*-0.975)*1000 as signed) insure ,b.game_no, " \            "case when a.score>0 then a.score*0.95*1000 else a.score*1000 end score_final " \            "from sdt_tmp_result a,sdt_tmp_result_step_1 b "\            "where a.user_name=b.user_name "\            "and a.type=\"保险收益\"" \            "and a.game_no=b.game_no " \            "and a.game_no=%s"        tmp_gameno=[gameno,gameno]        cursor.execute(strsql,tmp_gameno)        strsql="commit"        cursor.execute(strsql)        strsql="insert into sdt_tmp_result_step_3 (user_id,account_id,user_name,club_id,club_name,score,income_water,waterup,"\			"insure,income_insure,insure_up,income_total,up_total,delivery,game_no,score_final) "\            "select a.user_id,a.account_id, a.user_name,a.club_id,a.club_name,a.score ,a.income income_water, "\            "cast(abs(a.score)*0.025-a.income  as signed) waterup, "\            "b.score insure,b.income income_insure,cast((b.score*-0.975-b.income) as signed) insure_up,a.income+b.income income_total, "\            "cast((abs(a.score)*0.025-a.income+(b.score*-0.975-b.income)) as signed) up_total, "\			"cast((a.score_final+a.income+b.income) as signed) delivery,a.game_no,a.score_final "\            "from (select * from sdt_tmp_result_step_2 where type=\"总收益\") as a, "\            "(select * from sdt_tmp_result_step_2 where type=\"保险收益\") as b "\            "where a.user_id=b.user_id and a.game_no=b.game_no and a.game_no=%s "        cursor.execute(strsql, gameno)        strsql="commit"        cursor.execute(strsql)        strsql="select user_name,club_name,round(income_water/1000,2) income_water, "\            "round(score/1000,2) score,round(waterup/1000,2) waterup,round(insure/1000,2) insure, "\            "round(income_insure/1000,2) income_insure,round(insure_up/1000,2) insure_up, "\            "round(income_total/1000,2) income_total,round(up_total/1000,2) up_total, "\            "round(delivery/1000,2) delivery "\            "from sdt_tmp_result_step_3 a where a.game_no=%s"        cursor.execute(strsql, gameno)        try:            tb_result=cursor.fetchall()        except Exception as e:            return e    return tb_resultdef result_record(gameno):    if ucs_result_table_l1.objects.filter(game_no= gameno).exists():        return False    else:        with connection.cursor() as cursor:            strSQL="insert into sdt_ucs_result_table_l1(user_id,account_id,user_name,club_id,club_name,score,score_final,income_water, "\                "waterup,insure,income_insure, insure_up,income_total,up_total,delivery,game_no,operator_id,active_time,inactive_time,note) "\                "select a.user_id,a.account_id,a.user_name,a.club_id,a.club_name,a.score,a.score_final,a.income_water, "\                "a.waterup,a.insure,a.income_insure,a.insure_up,a.income_total,a.up_total,a.delivery,a.game_no,'30001',now(),'2037-01-01','测试数据' "\                "from sdt_tmp_result_step_3 a where a.game_no= %s "            cursor.execute(strSQL, gameno)        return Truedef gamenolist():    gamelist=ucs_result_table_l1.objects.filter(inactive_time='2037-01-01').values("game_no").distinct()    return gamelistdef club_check(club_name):    isexist=True    try:        ucs_subs_club.objects.filter(club_name=club_name).get(inactive_time="2037-01-01")    except :        isexist = False        return isexist    return isexistdef user_check(user_name):    isexist=True    try:        ucs_subs_user.objects.filter(user_name=user_name).get(inactive_time="2037-01-01")    except :        isexist=False        return isexist    return isexistdef result_searchByclub(club_id,starttime,endtime):    with connection.cursor() as cursor:        strSQL = "select a.game_no,date_format(a.active_time,'%%c-%%d %%H:%%i') record_time, "\                 "round(sum(a.score_final)/1000,2) score_final, "\                 "count(*) cnt, "\                 "round(sum(a.income_water)/1000,2) income_water, "\                 "round(sum(a.income_insure)/1000,2) income_insure, "\                 "round(sum(a.income_total)/1000,2) income_total, "\                 "round(sum(a.up_total)/1000,2) up_total, "\                 "round(sum(a.delivery)/1000,2) delivery "\                 "from sdt_ucs_result_table_l1 a "\                 "where a.club_id=%s "\                 "and date_format(a.inactive_time,'%%Y')='2037' "\                 "and a.active_time BETWEEN %s and %s "\                 "group by game_no,date_format(a.active_time,'%%c-%%d %%H:%%i')"        tmp_parm = [club_id, starttime, endtime]        cursor.execute(strSQL, tmp_parm)        tb_result=cursor.fetchall()    return  tb_resultdef result_searchByclubSum(club_id,starttime,endtime):    with connection.cursor() as cursor:        strSQL = "select "\                 "round(sum(a.score_final)/1000,2) score_final, "\                 "count(*) cnt, "\                 "round(sum(a.income_water)/1000,2) income_water, "\                 "round(sum(a.income_insure)/1000,2) income_insure, "\                 "round(sum(a.income_total)/1000,2) income_total, "\                 "round(sum(a.up_total)/1000,2) up_total, "\                 "round(sum(a.delivery)/1000,2) delivery "\                 "from sdt_ucs_result_table_l1 a "\                 "where a.club_id=%s " \                 "and a.active_time BETWEEN %s and %s " \                 "and date_format(a.inactive_time,'%%Y')='2037' "        tmp_parm = [club_id, starttime, endtime]        cursor.execute(strSQL, tmp_parm)        tb_result=cursor.fetchall()    return  tb_resultdef result_searchUnionbyclub(starttime,endtime):    with connection.cursor() as cursor:        strSQL = "select a.club_id,a.club_name, "\                "count(distinct a.game_no) game_cnt, "\                "round(sum(a.score_final)/1000,2) score_final, "\                "count(*) player_cnt, "\                "round(sum(a.income_water)/1000,2) income_water, "\                "round(sum(a.income_insure)/1000,2) income_insure, "\                "round(sum(a.income_total)/1000,2) income_total, "\                "round(sum(a.up_total)/1000,2) up_total, "\                "round(sum(a.delivery)/1000,2) delivery "\                "from sdt_ucs_result_table_l1 a " \                "where  a.active_time BETWEEN %s and %s "\                "and date_format(a.inactive_time,'%%Y')='2037' "\                "group by club_id,club_name" \                " order  by club_id asc"        tmp_parm=[starttime, endtime]        cursor.execute(strSQL, tmp_parm)        tb_result =cursor.fetchall()    return tb_resultdef result_searchUnionbyclubsum(starttime,endtime):    with connection.cursor() as cursor:        strSQL = "select "\                "count(distinct a.game_no) game_cnt, "\                "round(sum(a.score_final)/1000,2) score_final, "\                "count(*) player_cnt, "\                "round(sum(a.income_water)/1000,2) income_water, "\                "round(sum(a.income_insure)/1000,2) income_insure, "\                "round(sum(a.income_total)/1000,2) income_total, "\                "round(sum(a.up_total)/1000,2) up_total, "\                "round(sum(a.delivery)/1000,2) delivery "\                "from sdt_ucs_result_table_l1 a " \                "where  a.active_time BETWEEN %s and %s "\                "and date_format(a.inactive_time,'%%Y')='2037' "        tmp_parm=[starttime, endtime]        cursor.execute(strSQL, tmp_parm)        tb_result =cursor.fetchall()    return tb_result