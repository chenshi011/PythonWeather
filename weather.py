#!/usr/local/bin/python2.7
# -*- coding:utf-8 -*- 
'''
@author:     cs
'''
import sqlite3, urllib, re, time  
  
y = time.strftime("%Y")  
m = time.strftime("%m")  
d = time.strftime("%d")  
  
now = y + '-' + m + '-' + d  
todaylow = 99;  
todayhigh = 99;  
  
print now  
  
def getHtml(url):  
    page = urllib.urlopen(url)  
    html = page.read()  
    return html  
  
def getRel(html, reg):  
    mre = re.compile(reg)  
    relList = re.findall(mre, html)  
    return relList  
  
html = getHtml("http://weather.com.cn/weather/101021300.shtml")  
print html
reg1 = r'<p class="tem">\s<span>(.+)</span>/<i>(.+)℃</i>'  # temputer   
reg2 = r'</span>\s</em>\s<i>(.+)</i>'  # wind  
reg3 = r'class="wea">(.+)</p>\s<p class="tem">'  # index     
  
temputer = getRel(html, reg1)  
todayhigh = temputer[0][0]  
todaylow = temputer[0][1]  
i = 0  
j = 0  
for tmp in temputer:
    tmp = tmp[0] + "℃~" +tmp[1] + "℃"  
print temputer
wind = getRel(html, reg2)  
index = getRel(html, reg3)
mlist = temputer + index + wind  
  
_mlist = ['temp1', 'temp2', 'temp3', 'temp4', 'temp5', 'temp6', 'temp7', 'weather1', 'weather2', 'weather3', 'weather4', 'weather5', 'weather6', 'weather7', 'wind1', 'wind2', 'wind3', 'wind4', 'wind5', 'wind6', 'wind7', 'index', 'index48_d']  

#write file
f = open(r'%s.json' % str(now), 'w')  
f.write('{\"weatherinfo\":{\"city\":\"浦东\",\"city_en\":\"pudong\",\"date_y\":\"' + y + '年' + m + '月' + d + '日\",')  
size = len(mlist)  
for i in range(0, size - 1):  
    f.write('\"' + _mlist[i] + '":"' + str(mlist[i]) + '",')  
f.write('\"' + _mlist[size - 1] + '":"' + mlist[size - 1] + '"' + '}}')  
  
f.close()  

#insert Database
try:  
    table_name = "temputer"
    conn = sqlite3.connect('weather.db')
    cur = conn.cursor()  
    cur.execute('select name from sqlite_master where type="table" and name = "%s"' % table_name)
    value = cur.fetchone()
    if value is None:
        cur.execute('create table %s (time varchar(20) primary key, low varchar(20), high varchar(20))' % table_name)
    else:
        print "table %s already exists" % table_name
    sql = 'insert into %s(time,low,high) values(\'%s\',%s,%s)' % (table_name, now, todaylow, todayhigh)
    print sql
    cur.execute(sql)  
    conn.commit()  
    cur.close()  
    conn.close()  
except sqlite3.Error, e:  
    print "sqlite3 Error %d: %s" % (e.args[0], e.args[1])  
      
print 'insert Database Success'  
