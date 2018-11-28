from django.db import models
 
class cer_company(models.Model):
    SN = models.CharField(max_length=20,null=True,blank=True)                                     #编号
    Times = models.IntegerField(default= 0,null=True,blank=True)                                  #来样次数
    EAN = models.CharField(max_length=20,null=True,blank=True,default="NULL")                     #厂商识别代码
    CompanyName = models.CharField(max_length=20,null=True,blank=True,default="NULL")             #企业名称
    CompanyAddress = models.CharField(max_length=400,null=True,default="NULL")                    #企业地址
    Licence = models.CharField(max_length=200,null=True,blank=True,default="NULL")                #营业执照号码
    Corp = models.CharField(max_length=200,null=True,blank=True,default="NULL")                   #法人
    Postal = models.CharField(max_length=20,null=True, blank=True,default="NULL")                 #邮政编码 
    RecDate = models.DateTimeField(null=True, blank=True)                                         #初次受理时间
    GiveDate = models.DateTimeField(null=True, blank=True)                                        #来样时间
    RestAmount = models.IntegerField(default= 0, null=True, blank=True)                           #剩余数量
    UsedAmount = models.IntegerField(default= 0, null=True, blank=True)                           #使用数量
    SuccessAmount = models.IntegerField(default= 0,null=True, blank=True)                         #成功数量
    Contactor = models.CharField(max_length=20,null=True, blank=True,default="NULL")              #联系人
    ContactTel = models.CharField(max_length=20,null=True, blank=True,default="NULL")             #联系电话（方式）
    status = models.NullBooleanField(default=False,null=True, blank=True)                         #处理状态
    itemAmount = models.IntegerField(default= 0, null=True, blank=True)                           #来样数量（适用于企业来样）
    remarks = models.CharField(max_length=200,null=True,blank=True,default="/")                   #信息备注
    remarks = models.CharField(max_length=200,null=True,blank=True,default="/")                   #信息备注
    Sendstatus = models.NullBooleanField(default=False,null=True)                                 #邮寄状态
    SendDate = models.DateTimeField(null=True, blank=True)                                        #邮寄时间
    SendSN = models.CharField(max_length=200,null=True,blank=True,default=" ")                    #信息备注

class serial(models.Model):
    sn = models.IntegerField(default= 0,null=True,blank=True)                                     #企业序列SN 每月初变1
    time = models.DateTimeField(auto_now=True,null=True, blank=True)                              #时间戳1
    omb = models.CharField(max_length=20,null=True, blank=True)                                   #备用

'''
class JCFirm_copy(models.Model):                                                                 #copy
	F_id = models.CharField(blank=True,max_length=200 )
	firm_name = models.CharField(blank=True,max_length = 200 )
	firm_name1 = models.CharField(blank = True,max_length = 200 )
	register_address = models.CharField(blank = True,max_length = 200 )
	register_address1 = models.CharField(blank = True,max_length = 200 )
	register_postalcode = models.CharField(blank = True,max_length=200 )
	address = models.CharField(blank = True,max_length = 200)
	address1 = models.CharField(blank = True,max_length = 200)
	postcode = models.CharField(blank = True,max_length=200)
	certificate_code = models.CharField(blank = True,max_length = 50)
	political = models.CharField(blank = True,max_length=200)
	register_principal = models.CharField(blank = True,max_length=200)
	coin_type = models.CharField(blank = True,max_length=200)
	firm_type = models.CharField(blank = True,max_length=200)
	dm = models.CharField(blank = True,max_length=200)
	t_j_dm = models.CharField(blank = True,max_length=200 )
	firm_code = models.CharField(blank = True,max_length=200 )
	leader = models.CharField(blank = True,max_length=200)
	leader_tele = models.CharField(blank = True,max_length=200)
	leader_handset = models.CharField(blank = True,max_length=200)
	contactman = models.CharField(blank = True,max_length = 200)
	contactman_ctqh = models.CharField(blank = True,max_length = 200)
	contactman_tele = models.CharField(blank = True,max_length = 200)
	contactman_mp = models.CharField(blank = True,max_length = 200)
	contactman_fax = models.CharField(blank = True,max_length = 200)
	contactman_email = models.CharField(blank = True,max_length = 100)
	net_station = models.CharField(blank = True,max_length = 200)
	wishused_num = models.CharField(blank = True,max_length = 200)
	login_date = models.CharField(blank = True,max_length = 200)
	receiveflag = models.CharField(blank = True,max_length = 200)
	used_num = models.CharField(blank = True,max_length = 200)
	branch_code = models.CharField(blank = True,max_length = 200)
	dbd_code = models.CharField(blank = True,max_length = 200)
	Status = models.CharField(blank = True,max_length = 200)
	mdate = models.CharField(blank = True,max_length = 200)
	used_desc = models.CharField(blank = True,max_length = 200)
'''

class irm_copy(models.Model):                                                                 #Firm_copy
    F_id = models.CharField(blank=True,max_length=200 )
    firm_name = models.CharField(blank=True,max_length = 200,null=True,)
    register_address = models.CharField(blank = True,max_length = 200,null=True,)
    address = models.CharField(blank = True,max_length = 400,null=True,)
    postcode = models.CharField(blank = True,max_length=200,null=True,)
    certificate_code = models.CharField(blank = True,max_length = 50,null=True,)
    code = models.CharField(blank = True,max_length = 50,null=True,)