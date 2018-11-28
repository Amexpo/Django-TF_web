# -*- coding: utf-8 -*-
"""
@author: yangyanhao
"""

from django.shortcuts import render
from db.models import cer_company
from db.models import serial
from db.models import irm_copy
from django.db import connection, transaction
import datetime,time

################################################################################## db_in ######################################################################################################

def db_in(request):
    db_ctx={}
    if request.POST:
        if 'record_create' in request.POST:
            co_name = request.POST['co_name']
            co_contect = request.POST['co_contect']
            co_tel = request.POST['co_tel']
            co_num = request.POST['co_num']
            judge_exist = cer_company.objects.filter(CompanyName=co_name)
            if len(judge_exist) == 0:
                try:
                    ser = serial.objects.get(id='1')
                    nowtime = datetime.datetime.now()
                    if (nowtime.year*12+nowtime.month) > (ser.time.year*12 + ser.time.month):
                        sn = 1
                    else:
                        sn = ser.sn + 1
                    ser.sn = sn
                    ser.time = datetime.datetime.now()
                    ser.save()
                    create_sn = str(nowtime.year*100000 + nowtime.month * 1000 + sn)
                    cer_company.objects.create(CompanyName = co_name ,Contactor = co_contect, ContactTel = co_tel, RestAmount = co_num, SN = create_sn, RecDate = datetime.datetime.now(),status = 1)
                    db_ctx['create']= '<hr>创建企业信息记录成功！</br>企业名称：'+co_name+'</br>编号：'+ create_sn
                except BaseException as error1:
                    db_ctx['create']='Error: '+str(error1)
            else:
                db_ctx['create'] = co_name+'已存在.</br>编号：'+cer_company.objects.get(CompanyName=co_name,Times = '0').SN

        elif 'record_update' in request.POST:
            item_sn = request.POST['item_sn']
            item_name = request.POST['item_name']
            item_ean = request.POST['item_ean']
            for_count=[]
            search_list = cer_company.objects.filter(CompanyName__contains=item_name,SN__contains=item_sn,EAN__contains=item_ean)
            for items in search_list:
                for_count.append(items.CompanyName)
            if len(set(for_count)) != 1:
                db_ctx['update']='查询错误，请核对信息。可能原因：</br>1.无查找内容. </br>2.存在多个查找内容.'
            else:
                try:
                    TimesGet = len(cer_company.objects.filter(CompanyName__contains=item_name,SN__contains=item_sn,EAN__contains=item_ean))-1
                    dic = cer_company.objects.filter(CompanyName__contains=item_name,SN__contains=item_sn,EAN__contains=item_ean,Times = TimesGet)[0]
                    if dic.RestAmount < int(request.POST['item_count']):
                        db_ctx['update']= '该企业剩余数量（'+str(dic.RestAmount)+'条）不足，请先增加委托数量。'
                    else:
                        insert_SN = dic.SN
                        insert_EAN = dic.EAN
                        insert_CompanyName = dic.CompanyName
                        insert_CompanyAddress = dic.CompanyAddress
                        insert_Licence = dic.Licence
                        insert_Corp = dic.Corp
                        insert_RecDate = dic.RecDate
                        insert_GiveDate = datetime.datetime.now()
                        insert_RestAmount = dic.RestAmount
                        insert_UsedAmount = 0
                        insert_SuccessAmount = 0
                        insert_Contactor = dic.Contactor
                        insert_ContactTel = dic.ContactTel
                        insert_status = 0
                        insert_Times = len(for_count)
                        insert_itemAmount = request.POST['item_count']
                        cer_company.objects.create(SN=insert_SN ,
                                           EAN = insert_EAN,
                                           CompanyName = insert_CompanyName,
                                           CompanyAddress = insert_CompanyAddress,
                                           Licence = insert_Licence,
                                           Corp = insert_Corp,
                                           GiveDate = insert_GiveDate,
                                           RestAmount = insert_RestAmount,
                                           UsedAmount = insert_UsedAmount,
                                           SuccessAmount = insert_SuccessAmount,
                                           Contactor = insert_Contactor,
                                           ContactTel = insert_ContactTel,
                                           status = insert_status,
                                           RecDate = insert_RecDate,
                                           Times = insert_Times,
                                           itemAmount = insert_itemAmount
                                           )
                        db_ctx['update']='添加数据成功。</br>企业名称：'+insert_CompanyName+'</br>目前来样次数：'+str(insert_Times)         
                except BaseException as error2:
                    db_ctx['update']='Error:'+str(error2)
    return render(request, "db_in.html",db_ctx)

################################################################################ co_print ####################################################################################################

def co_print(request):
    ctx ={}
    ctx['rlt'] = '<div><h2>&emsp;打印展示界面</br></div>'
    qyxx={}
    if request.POST:             
        if 'qy_search' in request.POST:                          #按钮post------>搜索
            insert_code=''
            company_list=[]
            search_content=request.POST['qy_search']
            db_search= cer_company.objects.filter(CompanyName__icontains=search_content).order_by('SN')
            size=len(db_search)
            if size == 0:
                qyxx['fieldset']='&nbsp;&nbsp;无所查找记录，请核对。'
            else:
                for k in range(0,size):
                    if db_search[k].CompanyName not in company_list:
                        insert_code+='</fieldset><fieldset style="border-width: 1px; border-color:#ACD6FF;"><legend>'+db_search[k].CompanyName+'</legend>'
                        if db_search[k].Times!=0:
                            insert_code+='<input type="radio" name="m_id" id="m_id0" value = "'+db_search[k].SN+'-'+str(db_search[k].Times)+'">'+db_search[k].SN+'-'+str(db_search[k].Times)+'</br>'
                        company_list.append(db_search[k].CompanyName)
                    else:
                        if db_search[k].Times!=0:
                            insert_code+='<input type="radio" name="m_id" id="m_id0" value ="'+db_search[k].SN+'-'+str(db_search[k].Times)+'">'+db_search[k].SN+'-'+str(db_search[k].Times)+'</br>'
                insert_code+='</fieldset>'
                qyxx['fieldset']=insert_code
                qyxx['bt']='<input type="submit" class="a_demo_one" value="提交" name="qy_match" style="width:350px;margin-top:20px;">'
        elif 'qy_match' in request.POST:                        #按钮post----->左侧提交
            try:
                m_id=request.POST['m_id']                       #返回m_id
                db_get= cer_company.objects.get(SN=m_id[:9],Times=m_id[10:])
                ctx['c_num']= db_get.SN
                ctx['c_name'] = db_get.CompanyName
                ctx['c_address']= db_get.CompanyAddress
                ctx['c_left']= db_get.RestAmount
                ctx['c_suc']= db_get.SuccessAmount
                ctx['c_used']= db_get.UsedAmount
                ctx['c_eancode'] = db_get.EAN
                ctx['year']=db_get.GiveDate.year
                ctx['month']=db_get.GiveDate.month
                ctx['day']=db_get.GiveDate.day
                ctx['c_Times'] = db_get.Times
                ctx['c_Licence'] = db_get.Licence                #获取db的内容
            except(BaseException):
                pass
        elif 'tzs' in request.POST:                            #打印----->符合性确认通知书打印
            c_num = request.POST['c_num']                     #获取input的内容
            c_name = request.POST['c_name']
            c_address = request.POST['c_address']
            c_used = request.POST['c_used']
            c_left = request.POST['c_left']
            c_suc = request.POST['c_suc']
            year = request.POST['year'] 
            month = request.POST['month']
            day = request.POST['day']
            c_eancode = request.POST['c_eancode']
            c_Times = request.POST['c_Times']
            c_Licence = request.POST['c_Licence']
        
            ctx['rlt'] ='<div id="标题" style="text-align:center"><br><h1>使用商品条码符合性确认登记表通知书</h1></div>	<div id="信息"><HR align=center width=600 SIZE=1><p align="left" style="font-size:22px;line-height:130%;word-break:break-all">'\
                        '企业名称：<strong>'+c_name+'</strong></p><p align="left" style="font-size:22px;line-height:130%;word-break:break-all;text-indent:-5.5em;margin-left: 5.5em;">'\
                        '地&ensp;&ensp;&ensp;&ensp;址：<strong>'+c_address+'</strong></p>'\
                        '</p></div><div id="内容"><p style="text-indent:2em;font-size:22px;line-height:200%">贵企业在其产品上使用商品条码(详见附表),符合《广东省商品条码管理办法》第十四条的有关规定，现准予符合性确认。符合性确认证书与《中国商品条码系统成员》证书有效期相一致。</p><p style="text-indent:2em;font-size:22px;line-height:200%">'\
                        '本次符合性确认信息已使用数量<u>&ensp;'+c_used+'&ensp;</u>条，'\
                        '已确认数量<u>&ensp;'+c_suc+'&ensp;</u>条，'\
                        '未使用数量<u>&ensp;'+c_left+'&ensp;</u>条。</p><p align="right" style="text-indent:2em;font-size:22px;line-height:200%">'\
                        '办理日期:&nbsp;'+year+'年'+month+'月'+day+'日<br>（分支机构公章）&nbsp;&nbsp;&nbsp;&nbsp;</p></div><div id="注意事项"><p style="font-size:22px;line-height:100%">'\
                        '注意事项：</p><ol><li style="font-size:20px;line-height:200%">企业应确保在产品外包装上标示所使用商品条码的注册单位全称，否则一切后果企业自负。'\
                        '</li><li style="font-size:20px;line-height:200%">本备案只对附表中NO:商品条码的合法性进行确认，产品标签标识应按国家相关法律法规和标准执行。'\
                        '</li><li style="font-size:20px;line-height:200%">备案信息若有变更，请贵企业及时到所在地的编码分支机构重办理备案变更手续。</li></ol>'\
                        '</div><div id="结尾" style="text-align:center"><HR align=center width=650 SIZE=1><h4>中 国 物 品 编 码 中 心 深 圳 分 中 心 制</h4><br></div>'

            ctx['c_num']= c_num
            ctx['c_name']= c_name
            ctx['c_address']=c_address
            ctx['c_used']=c_used
            ctx['c_left']=c_left
            ctx['c_suc']= c_suc
            ctx['year']=year
            ctx['month']=month
            ctx['day']=day
            ctx['c_eancode'] = c_eancode
            ctx['c_Times'] = c_Times
            ctx['c_Licence'] = c_Licence                   #submit后传递input的value回去（符合性确认通知书打印）
        
        elif 'xxb' in request.POST:                         #打印----->企业办理信息表
            c_eancode = request.POST['c_eancode']
            c_num = request.POST['c_num']
            c_name = request.POST['c_name']
            c_address = request.POST['c_address']
            c_used = request.POST['c_used']
            c_left = request.POST['c_left']
            c_suc = request.POST['c_suc']
            c_Times = request.POST['c_Times']
            c_Licence = request.POST['c_Licence']
            year = request.POST['year']
            month = request.POST['month']
            day = request.POST['day']
            try:
                db_info_get= cer_company.objects.get(CompanyName=c_name,Times=0)
                G_year = str(db_info_get.RecDate.year)
                G_month = str(db_info_get.RecDate.month)
                G_day = str(db_info_get.RecDate.day)
                ctx['rlt'] = '<table border="1" bordercolor="black" cellspacing="0" ><tr><th  colspan="9" style="line-height:200%;text-indent:0.5em;height:50px;font-size:26px;">条码符合性确认企业办理信息表（境内）</th><tr><tr><td  colspan="9" style="line-height:200%;text-indent:0.5em;">'\
                             '条码符合性确认证书号：'+c_num+'</td></tr><tr><td  colspan="9" style="line-height:200%;text-indent:0.5em;">'\
                             '企业名称：'+c_name+'</td></tr><tr><td  colspan="9" style="line-height:200%;text-indent:0.5em;">'\
                             '企业地址：'+c_address+'</td></tr><tr><td  colspan="4" style="line-height:200%;text-indent:0.5em;">'\
                             '厂商识别代码：'+c_eancode+'</td><td  colspan="5" style="line-height:200%;text-indent:0.5em;">'\
                             '初次办理日期：'+G_year+'年'+G_month+'月'+G_day+'日</td></tr><tr><td align="center" style="width:45px;font-size:14px;height:40px;">序号</td><td align="center" style="width:150px;font-size:14px">商品条码目录表编号</td><td align="center" style="font-size:14px;">本次条码委托数量（条）</td><td align="center" style="font-size:14px;">办理条码数量（条）</td><td align="center" style="font-size:14px;">确认成功条码数量（条）</td><td align="center" style="font-size:14px;">剩余条码数量（条）</td><td align="center" style="width:80px;font-size:14px;">办理日期</td><td align="center" style="width:60px;font-size:14px;">经办人</td><td align="center" style="width:45px;font-size:14px;">归档</td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><tr><td style="text-align: center;height:25px;">&nbsp;</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>      <td></td></tr><td  colspan="9" style="line-height:200%;text-indent:0.5em;height:60px;">备注：</td></table>'
            except:
                year = ''
                month = ''
                day = ''
            ctx['c_num'] = c_num
            ctx['c_name']= c_name
            ctx['c_address']=c_address
            ctx['c_used']=c_used
            ctx['c_left']=c_left
            ctx['c_suc']= c_suc
            ctx['year']=year
            ctx['month']=month
            ctx['day']=day
            ctx['c_eancode'] = c_eancode
            ctx['c_Times'] = c_Times
            ctx['c_Licence'] = c_Licence                     #submit后传递input的value回去（企业办理信息表）

        elif 'page1' in request.POST:                            #打印----->证书首页
            c_num = request.POST['c_num']                     #获取input的内容
            c_name = request.POST['c_name']
            c_address = request.POST['c_address']
            c_used = request.POST['c_used']
            c_left = request.POST['c_left']
            c_suc = request.POST['c_suc']
            year = request.POST['year']
            month = request.POST['month']
            day = request.POST['day']
            c_eancode = request.POST['c_eancode']
            c_Times = request.POST['c_Times']
            c_Licence = request.POST['c_Licence']
            ctx['c_num'] = c_num
            ctx['c_name']= c_name
            ctx['c_address']=c_address
            ctx['c_used']=c_used
            ctx['c_left']=c_left
            ctx['c_suc']= c_suc
            ctx['year']=year
            ctx['month']=month
            ctx['day']=day
            ctx['c_eancode'] = c_eancode
            ctx['c_Times'] = c_Times
            ctx['c_Licence'] = c_Licence 
            
            ctx['rlt'] = '<div style="margin-top:20px;">'\
                         '<span style="line-height:280%;margin-left:180px;font-size:16px;">'+c_name+'</span>'\
                         '<br><span style="line-height:280%;margin-left:180px;font-size:16px;">'+c_num+'</span>'\
                         '<br><span style="line-height:280%;margin-left:180px;font-size:16px;">统一社会信用代码：'+c_Licence+'</span>'\
                         '</div>'
                         
        elif 'page2' in request.POST:                            #打印----->证书次页
            c_num = request.POST['c_num']                     #获取input的内容
            c_name = request.POST['c_name']
            c_address = request.POST['c_address']
            c_used = request.POST['c_used']
            c_left = request.POST['c_left']
            c_suc = request.POST['c_suc']
            year = request.POST['year']
            month = request.POST['month']
            day = request.POST['day']
            c_eancode = request.POST['c_eancode']
            c_Times = request.POST['c_Times']
            c_Licence = request.POST['c_Licence']
            ctx['c_num'] = c_num
            ctx['c_name']= c_name
            ctx['c_address']=c_address
            ctx['c_used']=c_used
            ctx['c_left']=c_left
            ctx['c_suc']= c_suc
            ctx['year']=year
            ctx['month']=month
            ctx['day']=day
            ctx['c_eancode'] = c_eancode
            ctx['c_Times'] = c_Times
            ctx['c_Licence'] = c_Licence 
            try:
                ctx['rlt'] = '<table class="gridtable" style="margin-left:-15px;margin-top:237px;width:850;">'
                empty_tr='<tr>'\
                         '<td style="width:37px;height:36.4px;" align="right"></td>'\
                         '<td style="width:130px;height:36.4px;" align="center"></td>'\
                         '<td style="width:81px;height:36.4px;" align="center"></td>'\
                         '<td style="width:85px;height:36.4px;" align="center"></td>'\
                         '<td style="width:298px;height:36.4px;" align="center"></td>'\
                         '<td style="width:129px;height:36.4px;" align="center"></td>'\
                         '<td style="width:80px;height:36.4px;" align="center"></td>'\
                         '</tr>'
                ctx['rlt']+=empty_tr * (int(c_Times)-1)
                ctx['rlt']+='<tr>'\
                            '<td style="width:37px;height:36.4px;" align="right">'+c_Times+'&nbsp;</td>'\
                            '<td style="width:130px;height:36.4px;" align="center">'+c_num+'-'+c_Times+'</td>'\
                            '<td style="width:81px;height:36.4px;" align="center">'+year+'.'+month+'.'+day+'</td>'\
                            '<td style="width:85px;height:36.4px;" align="center">'+c_suc+'</td>'\
                            '<td style="width:298px;height:36.4px;" align="center">与系统成员证书有效期一致</td>'\
                            '<td style="width:129px;height:36.4px;" align="center">薛瑶</td>'\
                            '<td style="width:80px;height:36.4px;" align="center">余'+c_left+'条</td>'\
                            '</tr>'
            except:
                pass
    else:
        pass
    
    
    
    return render(request, "print.html", {'ctx':ctx,
                                          'qyxx':qyxx,
                                          })

################################################################################## co_info ######################################################################################################

def co_info(request):
    ctx={}
    ctx['sum'] = len(cer_company.objects.filter(Times = 0))
    ctx['status']= len(cer_company.objects.filter(status = 0, Times__gt = 0))
    ctx['unsend']= len(cer_company.objects.filter(status = 1, Times__gt = 0, Sendstatus = 0))
    return render(request, "co_info.html",{'ctx':ctx
                                           })

################################################################################## item_info ######################################################################################################

def item_info(request):
    ctx={}
    ctx['sum'] = len(cer_company.objects.filter(Times = 0))
    ctx['status']= len(cer_company.objects.filter(status = 0, Times__gt = 0))
    ctx['unsend']= len(cer_company.objects.filter(status = 1, Times__gt = 0, Sendstatus = 0))
    return render(request, "item_info.html",{'ctx':ctx
                                           })    

############################################################################### 企业一览表 ###################################################################################################

def all_co(request):

    ####################################################################
    co_list = cer_company.objects.filter(Times = 0).order_by('-SN')
    ####################################################################
    list_copy=co_list[:]
    info_table=[]
    for value in list_copy:
        value.time = datetime.date.isoformat(value.RecDate)
        info_table.append(value)
    ###################################################################
    return render(request, "all_co.html",{'info_table':info_table,
                                          'co_list':co_list,
                                           })

################################################################################# 来样列表 ###################################################################################################

def item_come(request):
    ####################################################################
    co_list = cer_company.objects.filter(Times__gt = 0).order_by('-GiveDate')
    ####################################################################
    list_copy=co_list[:]
    info_table=[]
    for value in list_copy:
        value.serial = value.SN + '-' + str(value.Times)
        value.time = datetime.date.isoformat(value.GiveDate)

        #完成状态
        if value.status == 0:
            value.st = '<td bgcolor align="center" style="color:red;">未完成</td>'
            value.amount = '<td bgcolor style="color:red;" align="center">'+str(value.itemAmount)+'</td>'
        else:
            value.st = '<td bgcolor align="center" style="color:green;">已完成</td>'
            value.amount = '<td bgcolor style="color:green;" align="center">'+str(value.UsedAmount)+'</td>'
        #邮寄状态
        if value.Sendstatus == 0:
            value.Sendstatus = '<td bgcolor align="center" style="color:red;">未发</td>'
        else:
            value.Sendstatus = '<td bgcolor align="center" style="color:green;">已发</td>'
        info_table.append(value)
    ###################################################################
    return render(request, "item_come.html",{'info_table':info_table,
                                          'co_list':co_list,
                                           })

################################################################################# 信息查询 ###################################################################################################

def info_search(request):
    table={}
    table['code']=''
    table['bt'] = ''
    if request.POST:
        info_search = request.POST['info_search']
        if 'search_co_items' in request.POST:                 #企业来样查询
            co_list = cer_company.objects.filter(Times = 0, CompanyName__contains = info_search).order_by('-GiveDate')
            for company in co_list:
                table['code']+="<table class= 'gridtable' style='margin:10px;margin-bottom:30px;'>"\
                               "<tr><td colspan='8' style='font-size:16px;'><strong>"\
                               +company.CompanyName+\
                               "</strong></tr></td><tr><th>确认编号</th><th>剩余数量</th><th>已用数量</th><th>成功数量</th><th>办理日期</th><th>完成状态</th><th style='width:100px;'>备注</th></tr>"
                sn = cer_company.objects.get(Times = 0 , CompanyName = company.CompanyName)
                each_list = cer_company.objects.filter(Times__gt = 0, SN = sn.SN).order_by('-GiveDate')
                copy_list =each_list[:]
                for items in copy_list:
                    items.time = datetime.date.isoformat(items.GiveDate)
                    table['code']+="<tr><td align='center'>"+items.SN+'-'+str(items.Times)+"</td><td align='center'>"+str(items.RestAmount)+"</td><td align='center'>"+str(items.UsedAmount)+"</td><td align='center'>"+str(items.SuccessAmount)+"</td><td align='center'>"+items.time+"</td>"
                    if items.status == 0:
                        table['code']+='<td bgcolor style="color:red;" align="center">未完成</td>'
                    else:
                        table['code']+='<td bgcolor style="color:green;" align="center">已完成</td>'
                    table['code']+='<td align="center">'+items.remarks+'</td></tr>'
            table['code']+="</table><br>"
        elif 'search_co_info' in request.POST:

            table['bt'] = "<div id='bt1'><a href='#' class='button next' onClick='printdiv("\
                          +'"div_print"'\
                          +");'>&emsp;打&emsp;&emsp;印&emsp;&emsp;</a></div>"

            table['code'] = '<div id="div_print" style="width: 650px;margin: 0 auto;background:white;padding:20px;">		<p align="right" style="line-height:20%;font-family:Times;">NO:</p>	<hr color = black size = 1>		<h1 style="text-align:center;letter-spacing:10px;">使用境内注册商品条码</br>符合性确认登记表</h1>		<p>（申办企业盖章）</p>		<h2 style="text-align:center">企业填写部分</h2>	<table border="1" bordercolor="black" cellspacing="0" >		<tr>			<td style="line-height:150%;width:100px;height:60px;text-align:center;">企业名称</td>			<td style="font-size:16px;width:250px;"></td>			<td style="line-height:150%;width:100px;height:60px;text-align:center;">营业执照</br>注册号</td>			<td style="font-size:16px;;width:250px;"></td>		</tr>		<tr>			<td style="line-height:150%;width:100px;height:60px;text-align:center;">地&emsp;址</td>			<td style="font-size:16px;;width:250px;"></td>			<td style="line-height:150%;width:100px;height:60px;text-align:center;">邮政编码</td>			<td style="font-size:16px;;width:250px;"></td>		</tr>		<tr>			<td style="line-height:150%;width:100px;height:60px;text-align:center;">法&emsp;定<br>代表人</td>			<td style="font-size:16px;;width:250px;"></td>			<td style="line-height:150%;width:100px;height:60px;text-align:center;">联系方式</td>			<td style="font-size:16px;;width:250px;"></td>		</tr>		<tr>			<td style="line-height:150%;width:100px;height:60px;text-align:center;">联系人</td>			<td style="font-size:16px;;width:250px;"></td>			<td style="line-height:150%;width:100px;height:60px;text-align:center;">联系方式</td>			<td style="font-size:16px;;width:250px;"></td>		</tr>		<tr>			<td style="line-height:150%;width:100px;height:60px;text-align:center;">电子邮箱</td>			<td style="font-size:16px;;width:250px;"></td>			<td style="line-height:150%;width:100px;height:60px;text-align:center;">企业网址</td>			<td style="font-size:16px;;width:250px;"></td>		</tr>		<tr>			<td style="line-height:150%;width:100px;height:60px;text-align:center;">备&emsp;&emsp;注</td>			<td colspan="3"></td>		</tr>	</table>		<h2 style="text-align:center">审核部门填写部分</h2>	<table border="1" bordercolor="black" cellspacing="0" >		<tr>			<td style="line-height:150%;width:100px;height:60px;text-align:center;">备案意见</td>			<td colspan="3"></td>		</tr>		<tr>			<td style="line-height:150%;width:100px;height:60px;text-align:center;">审&emsp;核</br>日&emsp;期</td>			<td></td>			<td style="line-height:150%;width:100px;height:80px;text-align:center;">审核部</br>门盖章</td>			<td></td>		</tr>	</table>		<p><strong>商品目录表：</strong>见后页附表《商品条码目录表》</p>		<p style="font-size:20px;text-align:center">中国物品编码中心深圳分中心</p>	</div>'
    return render(request, "info_search.html",{'table':table,
                                           })

    
#<td align='center'>"+items.CompanyName+"</td>
################################################################################# 信息查询 ###################################################################################################
def update_nums(request):
    unfinished_list = cer_company.objects.filter(Times__gt = 0, status = 0 ).order_by('GiveDate')
    attention =""
    if request.POST:
        try:
            SN_Times = request.POST['SN']
            Name = request.POST['Name']
            used = request.POST['used']
            sucess = request.POST['sucess']
            target_SN = SN_Times.split('-')[0]
            target_Times = SN_Times.split('-')[1]
            rest = int(cer_company.objects.filter( SN = target_SN, Times = target_Times)[0].RestAmount) - int(request.POST['used'])
            if len(cer_company.objects.filter( SN = target_SN, Times__lt = target_Times, status = 0 )) > 0 :
                attention ="<hr></hr><p>错误：请处理先前来样。</p>"
            else:
                if rest < 0:
                    attention ="<hr></hr><p>该企业剩余数量不足，请增加委托数量后尝试。</p>"
                else:
                    cer_company.objects.filter( SN = target_SN, Times = target_Times).update(UsedAmount=used,SuccessAmount=sucess,status = 1, RestAmount = rest)
                    cer_company.objects.filter( SN = target_SN, Times__gt = target_Times).update(RestAmount = rest)
        except:
            pass
    return render(request, "update_nums.html",{'unfinished_list':unfinished_list,
                                               'attention':attention,
                                           })
################################################################################# 信息查询 ###################################################################################################
def update_qy(request):
    feedback=''
    error=''
    if request.POST:
        sn_change = request.POST['sn_change']
        name_change = request.POST['name_change']
        contactor_change = request.POST['contactor_change']
        tel_change = request.POST['tel_change']
        item_add = request.POST['item_add']
        co_lists =  cer_company.objects.filter(SN = sn_change)
        times = len(co_lists)

        if name_change !='':
            try:
                cer_company.objects.filter(SN = sn_change, Times = 0).update(CompanyName=name_change)
                cer_company.objects.filter(SN = sn_change, Times = (times-1)).update(CompanyName=name_change)
                feedback+= '企业名称变更：'+name_change+'<br>'
            except BaseException as error1:
                error+= '企业名称变更错误:'+str(error1)

        if contactor_change!='':
            try:
                cer_company.objects.filter(SN = sn_change, Times = 0).update(Contactor=contactor_change)
                cer_company.objects.filter(SN = sn_change, Times = (times-1)).update(Contactor=contactor_change)
                feedback+= '联系人变更：'+contactor_change+'<br>'
            except BaseException as error2:
                error+='联系人变更错误：'+str(error2)
        
        if tel_change!='':
            try:
                cer_company.objects.filter(SN = sn_change, Times = 0).update(ContactTel=tel_change)
                cer_company.objects.filter(SN = sn_change, Times = (times-1) ).update(ContactTel=tel_change)
                feedback+= '联系方式变更：'+tel_change+'<br>'
            except BaseException as error3:
                error+='联系方式变更错误：'+str(error3)
        
        if item_add!='':
            try:
                item_plus = int(cer_company.objects.filter(SN = sn_change, Times = (times-1))[0].RestAmount) + int(item_add)
                cer_company.objects.filter(SN = sn_change, Times = (times-1)).update(RestAmount=item_plus)
                feedback+= '新增：'+str(item_add)+'条<br>'
            except BaseException as error4:
                 error+='添加委托数量错误：'+str(error4)
        try:
            newremark =  cer_company.objects.filter(SN = sn_change, Times = (times-1))[0].remarks+feedback
            cer_company.objects.filter(SN = sn_change, Times = (times-1)).update(remarks = newremark)
        except BaseException as error5:
            error+=str(error5)
    return render(request, "update_qy.html",{'feedback':feedback,
                                             'error':error,
                                           })

###########################################################################################################
def page1(request):
    return render(request, "使用境内注册商品条码符合性确认登记表（新）.html")

################################################################################## func ######################################################################################################
def func(request):
    if request.POST:    
        '''
        from django.db import connection,transaction
        cursor = connection.cursor()
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        transaction.commit_unless_managed()
        '''
        cer_lists = cer_company.objects.filter(CompanyAddress = 'NULL')
        for updatecompany in cer_lists:
            try:
                x = irm_copy.objects.filter(firm_name = updatecompany.CompanyName)[0]
                updatecompany.CompanyAddress = x.address
                updatecompany.Postal = x.postcode
                updatecompany.Licence = x.certificate_code
                updatecompany.EAN = x.code
                updatecompany.save()
            except:
                pass
        sn2_update = serial.objects.get(id = 2)
        sn2_update.time = datetime.datetime.now()
        sn2_update.sn = irm_copy.objects.last().F_id
        sn2_update.save()
    return render(request, "functions.html")

###########################################################################################################

def update_send(request):
    unsend_list = cer_company.objects.filter(Times__gt = 0, status = 1, Sendstatus = 0 ).order_by('GiveDate')
    if request.POST:
        try:
            SN_Times = request.POST['SN']
            Name = request.POST['Name']
            SendSN = request.POST['SendSN']
            target_SN = SN_Times.split('-')[0]
            target_Times = SN_Times.split('-')[1]
            cer_company.objects.filter( SN = target_SN, Times = target_Times).update(Sendstatus = 1, SendDate =datetime.datetime.now(), SendSN = SendSN )
        except:
            pass
    return render(request, "update_send.html",{'unsend_list':unsend_list,
                                           })