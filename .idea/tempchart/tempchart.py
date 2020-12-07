from mysql import Mysql
from urllib import request
import urllib


#获得所有省份的CODE
def province_code():
    url = 'http://www.nmc.cn/f/rest/province'
    response = request.urlopen(url)
    page = response.read()
    page = bytes.decode(page)
    content = eval(page)
    p_code = {}
    for i in content:
        p_code[i['name']]=i['code']
    return p_code

#传入省份CODE，建个字典来存放该省份所有城市的CODE，再添加到总字典中
def city_code(all_cc,pd,province):
    url = 'http://www.nmc.cn/f/rest/province/'+province
    response = request.urlopen(url)
    page = response.read()
    page = bytes.decode(page)
    content = eval(page)
    for i in content:
        temp = {}
        temp['code'] = i['code']
        temp['province'] = pd
        all_cc[i['city']]=temp
    return all_cc

#循环所有省份，形成最终的城市code字典
def all_city_data():
    p_code = province_code()
    all_cc = {}
    for pd in p_code:
        all_cc = city_code(all_cc,pd,p_code[pd])
    return all_cc

#传入查询的城市，查询出该城市的天气情况
def find_code(city_name):
    all_cc = all_city_data()
    mysql = Mysql()
    for i in all_cc:
        city_name = i
        url = 'http://www.nmc.cn/f/rest/tempchart/'+all_cc[i]['code']
        response = request.urlopen(url)
        page = response.read()
        page = bytes.decode(page)
        content = eval(page)
        for i in content:
            sql = "insert into tempchart(city,cur_date,max_temp,min_temp) value "+"('"+city_name+"','"+str(i['time'])+"','"+str(i['max_temp'])+"','"+str(i['min_temp'])+"')"
        mysql.insert(sql)
        print('城市：'+city_name+','+'日期：'+str(i['time'])+','+'最高温度:%s,最低温度:%s' % (i['max_temp'],i['min_temp']))

if __name__ == '__main__':
    find_code("西安")