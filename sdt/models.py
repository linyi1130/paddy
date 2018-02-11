from django.db import models
import django.utils.timezone as timezone
# Create your models here.
class ucs_subs_club(models.Model):
    club_id = models.IntegerField(null=False)
    club_name = models.CharField(max_length=20)
    club_shortname = models.CharField(max_length=4)
    club_desc = models.CharField(max_length=80)
    club_lever=models.IntegerField(null=False)
    income_rate = models.IntegerField(null=False)
    insure_rate = models.IntegerField(null=False)
    active_time = models.DateTimeField(auto_now_add=True)
    inactive_time = models.DateTimeField(default='2037-1-1')


class ucs_subs_user(models.Model):
    num = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False)
    customer_id = models.IntegerField(null=True)
    account_id = models.IntegerField(null=True)
    user_name = models.CharField(max_length=20)
    wx_name = models.CharField(max_length=20)
    active_time = models.DateTimeField(auto_now_add=True)
    inactive_time = models.DateTimeField(default="2037-1-1")
    operator_id = models.IntegerField(null=True)
    note = models.CharField(null=True, max_length=40)


class ucs_club_user(models.Model):
    club_id = models.IntegerField(null=False)
    user_id = models.IntegerField(null=False)
    remark=models.CharField(null=True,max_length=20)
    feedback=models.IntegerField(default=0)
    feedback_type=models.IntegerField(default=0) #返水类型  0代表水上水下返水，1代表仅水上返水
    active_time = models.DateTimeField(auto_now_add=True)
    inactive_time = models.DateTimeField(default="2037-1-1")


class ucs_account(models.Model):
    account_id = models.IntegerField(null=False)
    user_id = models.IntegerField(null=False)
    club_id = models.IntegerField(null=False)
    account_level = models.IntegerField(null=True)
    active_time = models.DateTimeField(auto_now_add=True)
    inactive_time = models.DateTimeField(default='2037-1-1')


class real_user(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(null=False, max_length=20)
    active_time = models.DateTimeField(auto_now_add=True)


class real_account(models.Model):
    account_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    active_time = models.DateTimeField(auto_now_add=True)


class tmp_result(models.Model):
    user_name = models.CharField(max_length=20)
    type = models.CharField(max_length=10)
    score = models.IntegerField(null=False)
    game_no = models.CharField(max_length=40)





class pm_op_type(models.Model):
    op_type_id = models.IntegerField(null=True)
    op_type_name = models.CharField(max_length=20)
    inactive_time = models.DateTimeField(default='2037-1-1')


class pm_gametype(models.Model):
    type_id = models.IntegerField(null=True)
    type_name = models.CharField(max_length=10)
    type_desc=models.CharField(max_length=2)


class pm_blind(models.Model):
    blind_id = models.IntegerField(null=True)
    bigblind = models.CharField(max_length=20)
    blind_desc = models.CharField(max_length=20)
    type_desc = models.CharField(max_length=2)

class pm_ante(models.Model):
    blind_id = models.IntegerField(null=True)
    ante = models.IntegerField(null=True)
    type_desc = models.CharField(max_length=2)

class pm_gametime(models.Model):
    time_id = models.IntegerField(null=True)
    time_name = models.CharField(max_length=10)


class pm_gamepeople(models.Model):
    type_id = models.IntegerField(null=True)
    type_name = models.CharField(max_length=10)


class pm_game_status(models.Model):
    status_id=models.IntegerField(null=True)
    status=models.CharField(max_length=10)


class ucs_gameno(models.Model):
    gametime = models.DateTimeField(auto_now=True)
    cnt = models.IntegerField(null=True)
    game_no = models.CharField(max_length=20)


class ucs_gamerecord(models.Model):
    game_no = models.CharField(max_length=20)
    game_type = models.CharField(max_length=10)
    blind = models.CharField(max_length=10)
    ante = models.CharField(max_length=10)
    playercnt = models.IntegerField(null=False)
    buyin = models.IntegerField(null=True)
    duration = models.CharField(max_length=10)
    start_time = models.DateTimeField(auto_now=True)
    status_id = models.IntegerField(null=False)
    status = models.CharField(max_length=10)
    operator_id = models.IntegerField(null=True)
    inactive_time = models.DateTimeField(default='2037-01-01')
    straddle=models.IntegerField(default=0)
    group_name=models.CharField(max_length=10)
    record_time=models.DateTimeField(null=True)
    img_url=models.CharField(max_length=40)


class tmp_result_step_1(models.Model):
    user_id = models.IntegerField(null=False)
    account_id = models.IntegerField(null=False)
    user_name = models.CharField(max_length=20)
    club_id = models.IntegerField(null=False)
    club_name = models.CharField(max_length=20)
    income_rate = models.IntegerField(null=False)
    insure_rate = models.IntegerField(null=False)
    game_no = models.CharField(max_length=40)


class tmp_result_step_2(models.Model):
    user_id = models.IntegerField(null=False)
    account_id = models.IntegerField(null=False)
    club_id = models.IntegerField(null=False)
    club_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    score = models.IntegerField(null=False)
    score_final = models.IntegerField(null=False)
    income_rate = models.IntegerField(null=False)
    income = models.IntegerField(null=False)
    game_no = models.CharField(max_length=40)


class tmp_result_step_3(models.Model):
    user_id = models.IntegerField(null=False)
    account_id = models.IntegerField(null=False)
    user_name = models.CharField(max_length=20)
    club_id=models.IntegerField(null=False)
    club_name = models.CharField(max_length=20)
    score = models.IntegerField(null=False)            #原始成绩
    score_final = models.IntegerField(null=False)      #抽水后成绩
    income_water = models.IntegerField(null=False)     #水钱收入
    waterup = models.IntegerField(null=False)          #上交水钱
    insure = models.IntegerField(null=False)           #原始保险
    income_insure = models.IntegerField(null=False)    #抽水后保险
    insure_up = models.IntegerField(null=False)        #保险上交
    income_total = models.IntegerField(null=False)     #收入小计
    up_total = models.IntegerField(null=False)         #上交小计
    delivery = models.IntegerField(null=False)         #交收
    game_no = models.CharField(max_length=40)

class tmp_result_attachclub(models.Model):
    gameno = models.CharField(max_length=40)
    user_id = models.IntegerField(null=False)
    user_name = models.CharField(max_length=20)
    club_id = models.IntegerField(null=False)
    club_name = models.CharField(max_length=20)
    income_rate = models.IntegerField(null=False)
    insure_rate = models.IntegerField(null=False)

class tmp_result_attachclub_pre(models.Model):
    gameno = models.CharField(max_length=40)
    user_id = models.IntegerField(null=False)
    user_name = models.CharField(max_length=20)
    club_id = models.IntegerField(null=False)

class ucs_result_table_l1(models.Model):
    user_id = models.IntegerField(null=False)
    account_id = models.IntegerField(null=False)
    user_name = models.CharField(max_length=20)
    club_id = models.IntegerField(null=False)
    club_name = models.CharField(max_length=20)
    score = models.IntegerField(null= False)
    score_final = models.IntegerField(null=False)
    income_water=models.IntegerField(null=False)
    waterup = models.IntegerField(null=False)
    insure= models.IntegerField(null=False)
    income_insure = models.IntegerField(null=False)
    insure_up=models.IntegerField(null= False)
    income_total = models.IntegerField(null= False)
    up_total = models.IntegerField(null=False)
    delivery = models.IntegerField(null= False)
    game_no = models.CharField(max_length=40)
    operator_id = models.IntegerField(null=True)
    active_time = models.DateTimeField(default=timezone.now)
    inactive_time = models.DateTimeField(default='2037-01-01')
    flag=models.IntegerField(null=False)  #销账标志位 1代表已销账
    level=models.IntegerField(null=False)    #标志报表级别
    main_club_id=models.IntegerField(null=False)  #标志上交俱乐部ID
    reg_month=models.CharField(max_length=10)   #销账月份
    developer_id = models.IntegerField(null=True)#托管俱乐部ID
    is_modify=models.IntegerField(default=0)


class ucs_result_table_l2(models.Model):
    user_id = models.IntegerField(null=False)
    account_id = models.IntegerField(null=False)
    user_name = models.CharField(max_length=20)
    club_id = models.IntegerField(null=True)
    club_name = models.CharField(max_length=20)
    score = models.IntegerField(null= False)
    score_final = models.IntegerField(null=False)
    income_water=models.IntegerField(null=False)
    waterup = models.IntegerField(null=False)
    insure= models.IntegerField(null=False)
    income_insure = models.IntegerField(null=False)
    insure_up=models.IntegerField(null= False)
    income_total = models.IntegerField(null= False)
    up_total = models.IntegerField(null=False)
    delivery = models.IntegerField(null= False)
    feedback = models.IntegerField(null=False)
    game_no = models.CharField(max_length=40)
    operator_id = models.IntegerField(null=True)
    active_time = models.DateTimeField(default=timezone.now)
    inactive_time = models.DateTimeField(default='2037-01-01')
    flag=models.IntegerField(null=False)  #销账标志位 1代表已销账
    level=models.IntegerField(null=False)    #标志报表级别
    main_club_id=models.IntegerField(null=False)  #标志上交俱乐部ID
    reg_month=models.CharField(max_length=10)   #销账月份
    developer_id = models.IntegerField(null=True)
    is_modify = models.IntegerField(default=0)#0代表未修改过，1代表修改后原纪录，2代表修改后冲正记录

#分账前返水临时表
class ucs_result_table_l2_tmp(models.Model):
    user_id = models.IntegerField(null=False)
    account_id = models.IntegerField(null=False)
    user_name = models.CharField(max_length=20)
    club_id = models.IntegerField(null=True)
    club_name = models.CharField(max_length=20)
    score = models.IntegerField(null= False)
    score_final = models.IntegerField(null=False)
    income_water=models.IntegerField(null=False)
    waterup = models.IntegerField(null=False)
    insure= models.IntegerField(null=False)
    income_insure = models.IntegerField(null=False)
    insure_up=models.IntegerField(null= False)
    income_total = models.IntegerField(null= False)
    up_total = models.IntegerField(null=False)
    delivery = models.IntegerField(null= False)
    game_no = models.CharField(max_length=40)
    operator_id = models.IntegerField(null=True)
    active_time = models.DateTimeField(default=timezone.now)
    inactive_time = models.DateTimeField(default='2037-01-01')
    flag=models.IntegerField(null=False)  #销账标志位 1代表已销账
    level=models.IntegerField(null=False)    #标志报表级别
    main_club_id=models.IntegerField(null=False)  #标志上交俱乐部ID
    reg_month=models.CharField(max_length=10)   #销账月份
    developer_id = models.IntegerField(null=True)
    is_modify = models.IntegerField(default=0)#0代表未修改过，1代表修改后原纪录，2代表修改后冲正记录

#二级账单分账临时表
class ucs_result_table_tmp(models.Model):
    user_id = models.IntegerField(null=False)
    account_id = models.IntegerField(null=False)
    user_name = models.CharField(max_length=20)
    club_id = models.IntegerField(null=True)
    club_name = models.CharField(max_length=20)
    score = models.IntegerField(null= False)
    score_final = models.IntegerField(null=False)
    income_water=models.IntegerField(null=False)
    waterup = models.IntegerField(null=False)
    insure= models.IntegerField(null=False)
    income_insure = models.IntegerField(null=False)
    insure_up=models.IntegerField(null= False)
    income_total = models.IntegerField(null= False)
    up_total = models.IntegerField(null=False)
    delivery = models.IntegerField(null= False)
    game_no = models.CharField(max_length=40)
    operator_id = models.IntegerField(null=True)
    active_time = models.DateTimeField(auto_now= True)
    inactive_time = models.DateTimeField(default='2037-01-01')
    flag=models.IntegerField(null=False)  #销账标志位 1代表已销账
    level=models.IntegerField(null=False)    #标志报表级别
    main_club_id=models.IntegerField(null=False)  #标志上交俱乐部ID
    reg_month=models.CharField(max_length=10)   #销账月份
    developer_id = models.IntegerField(null=True)


class ucs_result_table(models.Model):
    game_no=models.CharField(max_length=40)
    user_id=models.IntegerField(null=False)
    account_id=models.IntegerField(null=False)
    user_name=models.CharField(max_length=20)
    club_id=models.IntegerField(null=False)
    club_name=models.CharField(max_length=20)
    score=models.IntegerField(null=False)
    score_final=models.IntegerField(null=False)
    income_water=models.IntegerField(null=False)
    waterup = models.IntegerField(null=False)
    insure= models.IntegerField(null=False)
    income_insure = models.IntegerField(null=False)
    insure_up=models.IntegerField(null= False)
    income_total = models.IntegerField(null= False)
    up_total = models.IntegerField(null=False)
    delivery = models.IntegerField(null= False)
    operator_id = models.IntegerField(null=True)
    active_time = models.DateTimeField(default=timezone.now)
    inactive_time = models.DateTimeField(default='2037-01-01')



class ucs_credit_account(models.Model):
    account_id = models.IntegerField(null=False)
    club_id=models.IntegerField(null=False)
    credit_num = models.IntegerField(null = False)
    operator_id = models.IntegerField(null= False)
    active_time = models.DateTimeField(auto_now=True)
    inactive_time = models.DateTimeField(default='2037-01-01')
    note = models.CharField(max_length=80)


class ucs_credit_developer_account(models.Model):
    developer_id=models.IntegerField(null=False)
    club_id=models.IntegerField(null=False)
    credit_num=models.IntegerField(null=False)
    operator_id=models.IntegerField(null=False)
    note=models.CharField(max_length=80)
    active_time=models.DateTimeField(auto_now_add=True)
    inactive_time=models.DateTimeField(default='2037-01-01')


class ucs_game_freeze_record(models.Model):
    account_id = models.IntegerField(null=False)
    game_no=models.CharField(max_length=20)
    user_id = models.IntegerField(null=False)
    club_id = models.IntegerField(null=False)
    freeze_num = models.IntegerField(null=False)
    status=models.CharField(max_length=10,default="预占用")
    operator_id = models.IntegerField(null= False)
    active_time = models.DateTimeField(auto_now=True)
    unfreeze_time=models.DateTimeField()
    inactive_time = models.DateTimeField(default='2037-01-01')
    note = models.CharField(max_length=80)


class pm_account_type(models.Model):
    type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)
    inactive_time = models.DateTimeField(default='2037-01-01')


class ucs_cash_account(models.Model):
    account_id = models.IntegerField(null=False)
    type_id = models.IntegerField(null=False)
    account_name = models.CharField(max_length=20)
    group_id = models.IntegerField(null=True)
    club_id = models.IntegerField(null=True)
    inactive_time = models.DateTimeField(default='2037-01-01')


class ucs_operator_group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=20)
    club_id = models.IntegerField(null=False)
    active_time = models.DateTimeField(auto_now_add=True)
    inactive_time = models.DateTimeField(default='2037-01-01')


class ucs_operator(models.Model):
    operator_id = models.IntegerField(null=False)
    operator_name = models.CharField(max_length=20)
    login_id = models.CharField(max_length=20)
    password = models.CharField(max_length=80)
    club_id = models.IntegerField(null=True)
    group_id = models.IntegerField(null=True)
    developer_id = models.IntegerField(null=True)
    active_time = models.DateTimeField(auto_now_add=True)
    inactive_time = models.DateTimeField(default='2037-01-01')
    permission_group=models.IntegerField(null=True)
    is_active=models.BooleanField(default=True)

#俱乐部财务组账户ID表
class ucs_club_account(models.Model):
    account_id = models.IntegerField(null=False)
    club_id=models.IntegerField(null=False)
    type_id=models.IntegerField(null=False)
    group_id=models.IntegerField(null=False)
    active_time=models.DateTimeField(auto_now_add=True)
    inactive_time=models.DateTimeField(default='2037-01-01')
    account_desc=models.CharField(max_length=20)

#用户账户ID表
class ucs_balance(models.Model):
    account_id = models.IntegerField(null=True)
    user_id = models.IntegerField(null=True)
    club_id=models.IntegerField(null=True)
    balance = models.IntegerField(null=True)
    chance = models.IntegerField(null=True)
    type_id=models.IntegerField(null=True)
    chance_desc = models.CharField(null=False, max_length=20)
    serial_no = models.CharField(max_length=25)
    updatetime = models.DateTimeField(default=timezone.now)
    inactive_time = models.DateTimeField(default='2037-1-1')
    operator_id = models.IntegerField(null=True)
    note = models.CharField(max_length=80)

#俱乐部账户流水表
class ucs_club_balance(models.Model):
    serial_no = models.CharField(max_length=30)
    account_id = models.IntegerField(null=False)
    balance=models.IntegerField(null=False)
    chance=models.IntegerField(null=False)
    chance_type=models.IntegerField(null=True)
    chance_desc=models.CharField(max_length=20)
    operator_id=models.IntegerField(null=False)
    group_id= models.IntegerField(null=False)
    update_time =models.DateTimeField(auto_now_add=True)
    inactive_time=models.DateTimeField(default='2037-01-01')
    note=models.CharField(max_length=80)


#联盟账务流水表
class ucs_union_balance(models.Model):
    serial_no = models.CharField(max_length=30)
    account_id = models.IntegerField(null=False)
    balance=models.IntegerField(null=False)
    chance=models.IntegerField(null=False)
    chance_type=models.IntegerField(null=True)
    chance_desc=models.CharField(max_length=20)
    operator_id=models.IntegerField(null=False)
    group_id= models.IntegerField(null=False)
    update_time = models.DateTimeField(auto_now_add=True)
    inactive_time=models.DateTimeField(default='2037-01-01')
    note=models.CharField(max_length=80)
    main_club_id=models.IntegerField(null=False)

class ucs_union_balance_l1(models.Model):
    serial_no = models.CharField(max_length=30)
    account_id = models.IntegerField(null=False)
    balance=models.IntegerField(null=False)
    chance=models.IntegerField(null=False)
    chance_type=models.IntegerField(null=True)
    chance_desc=models.CharField(max_length=20)
    operator_id=models.IntegerField(null=False)
    group_id= models.IntegerField(null=False)
    update_time = models.DateTimeField(auto_now_add=True)
    inactive_time=models.DateTimeField(default='2037-01-01')
    note=models.CharField(max_length=80)
    main_club_id=models.IntegerField(null=False)


class ucs_union_account(models.Model):
    account_id=models.IntegerField(null=False)
    club_id=models.IntegerField(null=False)
    active_time=models.DateTimeField(auto_now_add=True)
    inactive_time=models.DateTimeField(default='2037-01-01')


class pm_club_lever(models.Model):
    lever_id=models.IntegerField(null=False)
    lever_name=models.CharField(max_length=20)


class ucs_club_relation(models.Model):
    club_id=models.IntegerField(null=False)
    subs_club_id=models.IntegerField(null=False)
    active_time=models.DateTimeField(auto_now_add=True)
    inactive_time=models.DateTimeField(default='2037-01-01')
    club_level=models.IntegerField(null=False)

#俱乐部收入户流水
class ucs_company_balance(models.Model):
    club_id=models.IntegerField(null=False)
    serial_no=models.CharField(max_length=30)
    balance=models.IntegerField(null=False)
    chance=models.IntegerField(null=False)
    op_type_id=models.IntegerField(null=False)
    operator_id=models.IntegerField(null=False)
    active_time=models.DateTimeField(auto_now_add=True)
    inactive_time=models.DateTimeField(default='2037-01-01')
    note=models.CharField(max_length=80)
    op_account_id=models.IntegerField(null=True)


#俱乐部收入户流水类型
class pm_company_type(models.Model):
    type_id=models.IntegerField(null=False)
    type=models.CharField(max_length=20)
    inactive_time=models.DateTimeField(default='2037-01-01')


#俱乐部牌局收益汇总表
class ucs_company_income(models.Model):
    club_id=models.IntegerField(null=False)
    water=models.IntegerField(null=False)
    insure=models.IntegerField(null=False)
    up_water=models.IntegerField(null=False)
    up_insure=models.IntegerField(null=False)
    active_time=models.DateTimeField(auto_now_add=True)
    inactive_time=models.DateTimeField(default='2037-01-01')


#俱乐部拉手发展表
class ucs_developer(models.Model):
    developer_id=models.IntegerField(null=False)
    developer_name=models.CharField(max_length=20)
    developer_desc=models.CharField(max_length=40)
    income_rate=models.IntegerField(null=False)
    insure_rate=models.IntegerField(null=False)
    club_id=models.IntegerField(null=False)
    active_time=models.DateTimeField(auto_now_add=True)
    inactive_time=models.DateTimeField(default='2037-01-01')


class ucs_club_developer(models.Model):
    user_id=models.IntegerField(null=False)
    developer_id=models.IntegerField(null=False)
    active_time=models.DateTimeField(auto_now_add=True)
    inactive_time=models.DateTimeField(default='2037-01-01')
    club_id=models.IntegerField(null=False)


class ucs_permission_group(models.Model):
    group_id=models.IntegerField(null=False)
    group_name=models.CharField(max_length=20)
    inactive_time=models.DateTimeField(default='2037-01-01')


class pm_permission(models.Model):
    type_id=models.IntegerField(null=False)
    permission=models.CharField(max_length=20)
    inactive_time = models.DateTimeField(default='2037-01-01')


class ucs_permission(models.Model):
    group_id=models.IntegerField(null=False)
    type_id=models.IntegerField(null=False)
    inactive_time = models.DateTimeField(default='2037-01-01')


class paddy_admin(models.Model):
    login_name=models.CharField(max_length=20)
    password=models.CharField(max_length=80)


class ucs_game_reward(models.Model):
    blind_id=models.IntegerField(null=False)
    type_id=models.IntegerField(null=False)
    reward = models.IntegerField(null=False)
    club_id=models.IntegerField(null=False)
    inactive_time=models.DateTimeField(default='2037-01-01')


class pm_reward(models.Model):
    type_id=models.IntegerField(null=False)
    type_name=models.CharField(max_length=20)
    inactive_time=models.DateTimeField(default='2037-01-01')

#账户提现手续费，rate单位万分位
class pm_deposit_rate(models.Model):
    account_type=models.IntegerField(null=False)
    rate=models.IntegerField(null=False)
    club_id=models.IntegerField(null=False)
    inactive_time=models.DateTimeField(default='2037-01-01')


class ucs_deposit_balance(models.Model):
    serial_no=models.CharField(max_length=40)
    club_id=models.IntegerField(null=False)
    group_id=models.IntegerField(null=False)
    account_id=models.IntegerField(null=False)              #俱乐部现金账户ID
    type_id=models.IntegerField(null=False)                 #俱乐部账户类型（支付宝，微信等）
    deposit=models.IntegerField(null=False)
    fee=models.IntegerField(null=False)
    operator_id=models.IntegerField(null=False)
    status_id=models.IntegerField(null=False)
    account_target_id=models.IntegerField(null=False)       #提现到银行卡账户ID
    active_time=models.DateTimeField(auto_now_add=True)
    inactive_time=models.DateTimeField(default='2037-01-01')


class pm_deposit_status(models.Model):
    status_id=models.IntegerField(null=False)
    status=models.CharField(max_length=20)
    inactive_time=models.DateTimeField(default='2037-01-01')


class ucs_developer_balance(models.Model):
    serial_no = models.CharField(max_length=40)
    developer_id=models.IntegerField(null=False)
    club_id=models.IntegerField(null=False)
    chance=models.IntegerField(null=False)
    balance=models.IntegerField(null=False)
    type_id=models.IntegerField(null=False)
    user_id=models.IntegerField(null=True)
    operator_id=models.IntegerField(null=False)
    note=models.CharField(max_length=40)
    active_time=models.DateTimeField(auto_now_add=True)
    inactive_time=models.DateTimeField(default='2037-01-01')



class menu_tree_l1(models.Model):
    tree_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=20,null=True)
    tree_desc=models.CharField(max_length=40,null=True)
    url=models.CharField(max_length=80,null=True)
    inactive_time=models.DateTimeField(default='2037-01-01')


class menu_tree_l2(models.Model):
    tree_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=20, null=True)
    tree_desc=models.CharField(max_length=40, null=True)
    parent_id=models.IntegerField(null=False)
    url=models.CharField(max_length=80, null=True)
    inactive_time=models.DateTimeField(default='2037-01-01')


class permission_menu(models.Model):
    group_id=models.IntegerField(null=False)
    tree_l1_id=models.IntegerField(null=True)
    tree_l2_id=models.IntegerField(null=True)
    inactive_time=models.DateTimeField(default='2037-01-01')


class ucs_game_reward_record(models.Model):
    game_no=models.CharField(max_length=30)
    file_url=models.CharField(max_length=20)
    club_id=models.IntegerField(null=False)
    blind_id=models.IntegerField(null=True)
    type_id=models.IntegerField(null=True)
    reward=models.IntegerField(null=False)
    operator_id=models.IntegerField(null=False)
    active_time=models.DateTimeField(default=timezone.now)
    inactive_time=models.DateTimeField(default='2037-01-01')


class operator_log(models.Model):
    operator_id=models.IntegerField(null=False)
    op_type_id=models.IntegerField(null=True)
    op_desc=models.CharField(max_length=100)
    active_time=models.DateTimeField(default=timezone.now)
