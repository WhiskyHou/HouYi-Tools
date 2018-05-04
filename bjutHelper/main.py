# encoding=gb2312

import re
import os
import requests
from urllib import parse
from lxml import etree
from bs4 import BeautifulSoup

username = input('username:')
password = input('password:')
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/63.0.3239.132 "
                  "Safari/537.36 "
}
index_url = 'http://gdjwgl.bjut.edu.cn/'
# index_url = 'http://gdjwgl.cjw1115.com/'

def getViewState(test):
    soup = BeautifulSoup(test, 'lxml')
    result = soup.find('input', attrs={'name': '__VIEWSTATE'})
    result = result['value']
    # print(result)
    return result


s = requests.session()

# 准备登录资源
pic = s.get(url=index_url+'CheckCode.aspx', headers=headers)
pic_file = open('ttttpic.jpg', 'wb')
pic_file.write(pic.content)
pic_file.close()
os.startfile('ttttpic.jpg')
code = input('check code:')

index_page = s.get(url=index_url+'default2.aspx', headers=headers)
viewstate = getViewState(index_page.text)

login_post_data = {
    '__VIEWSTATE': viewstate,
    'txtUserName': username,
    'TextBox2': password,
    'txtSecretCode': code,
    'RadioButtonList1': '%D1%A7%C9%FA',
    'Button1': "",
    'lbLanguage': '',
    'hidPdrs': '',
    'hidsc': ''
}


# 登录请求
login_page = s.post(url=index_url+'default2.aspx', data=login_post_data, headers=headers)
catch = '<span id="xhxm">(.*?)</span></em>'
name = re.findall(catch, login_page.text)
name = name[0]
name = name[:-2]
name = str(name).replace(r'\x', '%')
# name.encode('gb2312')
# parse.quote(name)


# 查分界面请求
headers['Referer'] = index_url+'xs_main.aspx?xh='+username
content_page = s.get(url=index_url+'xscjcx.aspx?xh='+username+'&xm='+name+'&gnmkdm=N121605', headers=headers)
viewstate_content = getViewState(content_page.text)


# 查历年成绩请求
score_post_data = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': viewstate_content,
    'hidLanguage': '',
    'ddlXN': '1',
    'ddlXQ': '1',
    'ddl_kcxz': '',
    'btn_zcj': '历年成绩'
}
headers['Referer'] = index_url+'xscjcx.aspx?xh='+username+'&xm='+parse.quote(name)+'&gnmkdm=N121605'
score_page = s.post(url=index_url+'xscjcx.aspx?xh='+username+'&xm='+name+'&gnmkdm=N121605',
                    data=score_post_data,
                    headers=headers)


# 解析和计算历年成绩
html = score_page.text
soup_html = BeautifulSoup(html, 'lxml')
s = soup_html.find_all("tr")

array = []
for item in s:
    soup2 = BeautifulSoup(str(item), "lxml")
    s2 = soup2.find_all("td")
    temp = []
    for item2 in s2:
        item2 = str(item2).replace("<td>", "")
        item2 = str(item2).replace("</td>", "")
        item2 = str(item2).replace(" ", "", 6)
        temp.append(item2)
    # print(temp)
    array.append(temp)

course = 0
sum = 0
jidian_get = 0
credit_sum = 0
guake_num = 0
for p in array:
    # print(p)
    try:
        if p[5] == '第二课堂' or p[5] == '课程归属':
            continue
        # 这里筛选一下学年
        # if p[0] == '2017-2018':
        course += 1
        credit_sum += float(p[6])
        sum += float(p[8]) * float(p[6])
        jidian_get += float(p[7])
        # 这里算一下挂科数量
        if float(p[8]) < 60:
            guake_num += 1
    except:
        pass
average = sum / credit_sum
jidian = jidian_get / course

print('你好！'+name+'\n')
print("学分："+str(credit_sum)+"\n加权："+str(average)+"\n绩点："+str(jidian)+"\n挂科："+str(guake_num))
if os.path.exists('ttttpic.jpg'):
    os.remove('ttttpic.jpg')

push_url = 'http://r6.xxhouyi.cn/score.php'
push_data = {
    'name': name,
    'score': average,
    'guake': guake_num
}
push_response = requests.post(url=push_url, data=push_data)
push_text = push_response.text
print(push_text)

key = input("\n按Enter退出")
