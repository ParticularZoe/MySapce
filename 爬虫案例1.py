#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""code_info
@Time    : 2021 2021/7/22 10:02 上午
@Author  : keyoung
@File    : HousePrice_KM.py
"""


# ************        昆明市房价基本信息爬取     *******************

from bs4 import BeautifulSoup
import urllib.request,urllib.error
from pprint import pprint
import xlwt #倒入excel
import re
import requests

#正则匹配规则
#——————————————————————————————————————————————————————————————————————————————————————————————————————
re_name = re.compile(r'<a .* target="_blank">(.*)</a>')
re_phone = re.compile(r'<span>(.*?)</span>')
re_price = re.compile(r'<i>(\d*)</i>')
re_area = re.compile(r'<div class="m_list_hx"><span>(.*?)</span> </div>')
re_adress = re.compile(r'<span>地址：(.*)</span>')
re_date = re.compile(r'<i .*>有效期：(.*)</i>')
#——————————————————————————————————————————————————————————————————————————————————————————————————————

def get_html(url):
    head = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
    }
    r = requests.get(url,headers = head)
    if r.status_code == 200 :
        return r.text
    else:
        return ''

def get_data(baseurl):
    data = []   #存放每一页的信息
    for i in range(1,11):
        url = baseurl+'&page=' + str(i)
        html = get_html(url)
        # print(html)
        # 解析数据
        sp = BeautifulSoup(html,'html.parser')
        for a in sp.find_all('div',class_ = 'm_lp_list_r'):
            a = str(a)
            one = []    #保存一组信息
            #正则匹配
            #房地区域名
            name = re.findall(re_name,a)[0]
            one.append(name)
            # print(a)

            #电话
            phone = re.findall(re_phone,a)[0]
            one.append(phone)

            #均价 元/平方米
            price = re.findall(re_price,a)[0]
            one.append(price)

            #面积
            area = re.findall(re_area,a)[0]
            one.append(area)

            #地址
            adress = re.findall(re_adress,a)[0]
            one.append(adress)

            #有效期
            date = re.findall(re_date,a)[0]
            one.append(date)
            data.append(one)
    # pprint(data)
    return data

#存储信息excel
def saveData(list,savepath):
    print('save...... ')
    lens = len(list)
    book = xlwt.Workbook(encoding='utf-8',style_compression=False)
    #单元格
    sheet = book.add_sheet('昆明市房价信息',cell_overwrite_ok=True)#覆盖单元格
    #表格列信息
    col = ('房区位置','电话信息','价格信息(元/m2)','户型占地','地址信息','有效期')
    #写入第一行标题信息
    for i in range(0,6):
        cwidth = sheet.col(i).width
        if (len(col[i])*367) > cwidth:
            sheet.col(i).width = (len(col[i])*367)
        sheet.write(0,i,col[i])
    #填入对应信息
    for i in range(0,lens):
        temp = list[i]
        for j in range(0,6):
            #自动补全宽度
            cwidth = sheet.col(j).width
            if (len(temp[j])*367) > cwidth:
                sheet.col(j).width = (len(temp[j])*367)
            #写入信息
            sheet.write(i+1,j,temp[j])
        print("第 %d 条记录入成功！"%(i+1))
    book.save(savepath)

if __name__ == '__main__':
    baseurl = 'http://yunnan.huawuwang.com/house/search?py=kunmingshi&city=57&ly=baidu&kw=Y'
    path = '昆明市房价信息录入.xls'
    # html = get_html(url)
    # pprint(html)
    datalist = get_data(baseurl)
    # print(len(datalist))
    saveData(datalist,path)