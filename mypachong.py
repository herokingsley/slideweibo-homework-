#utf-8
# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import json
from bs4 import *

import re
#import MySQLdb
import sys

class WeiBo:
    #初始化基本信息,常用header
    def __init__(self):
        pass
    #to-do 创建个性的opener以免污染全局控件

    def login(self,uname,pwd):
    #登录微博函数
        cj = cookielib.LWPCookieJar()
        self.cookie_support = urllib2.HTTPCookieProcessor(cj)
        self.httpHandler = urllib2.HTTPHandler(debuglevel = 1)
        self.httpsHandler = urllib2.HTTPSHandler(debuglevel = 1);
        opener = urllib2.build_opener(self.cookie_support,self.httpHandler,self.httpsHandler)
        #to-do 改变这行     
        urllib2.install_opener(opener);
        post_data = {
         'uname':uname,
         'pwd':pwd,
         'backURL':'https://m.weibo.cn/',
         'check':'1'
        }
        url = 'https://m.weibo.cn/login?vt=4&wm=ig_0001_home'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header = {
           'User-Agent':user_agent,
           'Referer':'https://m.weibo.cn/login?vt=4&wm=ig_0001_home'
        }
        post_data = urllib.urlencode(post_data)
        req = urllib2.Request(url, post_data, header)
        response = urllib2.urlopen(req)
        the_page = response.read()
        print '登录····'
        mainSoup = BeautifulSoup(the_page)
        url = mainSoup.a.get('href')
        req = urllib2.Request(url,'',header)
        #req2.add_header('Cookie',cookie)
        page = urllib2.urlopen(req).read()
        print '跳转'
        return page
    
    #爬关注人微博函数
    def creep_weibo(user_uid):
        page_num = 2
        index = 1
        while (index <= page_num):
            header = {
                 'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            }
            #所有微博
#        url = 'http://m.weibo.cn/page/json?containerid=100505' + str(user_uid) + '_-_WEIBO_SECOND_PROFILE_WEIBO&rl=2&luicode=10000011&lfid=100505' + str(user_uid) + '&uicode=10000012&fid=100505' + str(user_uid) + '_-_WEIBO_SECOND_PROFILE_WEIBO&ext=sourceType%3A&page=' + str(index)
            #原创微博
            url = 'http://m.weibo.cn/page/json?containerid=100505' + str(user_uid) + '_-_WEIBO_SECOND_PROFILE_WEIBO_ORI&luicode=10000011&rl=2&lfid=100505' + str(user_uid) + '&uicode=10000012&fid=100505' + str(user_uid) + '_-_WEIBO_SECOND_PROFILE_WEIBO&ext=sourceType%3A&page=' + str(index)
            req = urllib2.Request(url,'',header)
            data = urllib2.urlopen(req).read()
            print '----------------获取到微博Json数组 page = ' + str(index) + ' 总共' + str(page_num) + '页----------------'
            dict = json.loads(data)
#        print dict
            if dict.get('ok',0) == 1:
                if index == 1:
                    page_num = dict.get('maxPage',0)
                mblogList = dict.get('mblogList',0)
                if mblogList != 0:
                    for mblog in mblogList:
                        retweet = mblog.get('retweeted_status',0)
                        if retweet == 0:
                            body = mblog.get('text')
                            bid = mblog.get('bid')
                            create_time = mblog.get('created_at')
                        
                            body = filter_tag(body)
                            body = body.encode('gbk', 'ignore').decode('gbk', 'ignore').encode('utf-8', 'ignore')
                            print body
                            #save_person_weibo(bid,user_uid,body,create_time)
                            #conn.commit()
                        else:
                            print '转发的滤掉······'
            index = index + 1

    #爬关注人用户列表函数
    def creep_follows(user_uid):
        page_num = 2
        index = 1
        while (index <= page_num):
            #粉丝列表
            header = {
                'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            }
            url = 'http://m.weibo.cn/page/json?module=user&action=FOLLOWERS&itemid=FOLLOWERS&title=%E5%85%B3%E6%B3%A8&containerid=100505' + str(user_uid) + '_-_FOLLOWERS&page=' + str(index)
            req = urllib2.Request(url,'',header)
            data = urllib2.urlopen(req).read()
        
            print '----------------获取到关注人列表Json数组 page = ' + str(index) + ' 总共' + str(page_num) + '页----------------'
        
            dict = json.loads(data)
#        print dict
            if dict.get('ok',0) == 1:
                print 'success'
                if index == 1:
                    page_num = dict.get('maxPage',0)
                users = dict.get('users',0)
                if users != 0:
                    for user in users:
                        uid = user.get('id')
                        name = user.get('screen_name')
                        sex = '男' if user.get('gender') == 'm' else '女'
                        fans_num = user.get('fansNum')
                        common = '无'
                        print name
                        #存到数据库的表person_info
                        #save_person_info(uid,name,sex,common,fans_num)
                        #conn.commit()
            index = index + 1;
    def search(keyword,type):
        http://m.weibo.cn/searchs/weibo?key=%E6%B1%82%E8%81%8C&&page=1;
        http://m.weibo.cn/searchs/user?q=%E6%B1%82%E8%81%8C&&page=1;
        pass;
    def 

class htmlTool:
     #正则表达式，过滤掉html标签
    def filter_tag(htmlstr):
        re_cdata = re.compile('<!DOCTYPE HTML PUBLIC[^>]*>', re.I)
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I) #过滤脚本
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I) #过滤style
        re_br = re.compile('<br\s*?/?>')
        re_h = re.compile('</?\w+[^>]*>')
        re_comment = re.compile('<!--[\s\S]*-->')
        s = re_cdata.sub('', htmlstr)
        s = re_script.sub('', s)
        s=re_style.sub('',s)
        s=re_br.sub('\n',s)
        s=re_h.sub(' ',s)
        s=re_comment.sub('',s)
        blank_line=re.compile('\n+')
        s=blank_line.sub('\n',s)
        s=re.sub('\s+',' ',s)
        s=replaceCharEntity(s)
        return s
   
    def replaceCharEntity(htmlstr):
        #这个应该直接可以用封装的函数解码urlencode吧.
        CHAR_ENTITIES={'nbsp':'','160':'',
            'lt':'<','60':'<',
            'gt':'>','62':'>',
            'amp':'&','38':'&',
            'quot':'"''"','34':'"'}
        re_charEntity=re.compile(r'&#?(?P<name>\w+);') #命名组,把 匹配字段中\w+的部分命名为name,可以用group函数获取
        sz=re_charEntity.search(htmlstr)
        while sz:
            #entity=sz.group()
            key=sz.group('name') #命名组的获取
            try:
                htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1) #1表示替换第一个匹配
                sz=re_charEntity.search(htmlstr)
            except KeyError:
                htmlstr=re_charEntity.sub('',htmlstr,1)
                sz=re_charEntity.search(htmlstr)
        return htmlstr

#重构 移除数据耦合.
#连接数据库
#try:
#    conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='test',port=3306,charset='utf8',use_unicode=False)
#    cur = conn.cursor();
#except MySQLdb.Error,e:
#    print "MySQL Error %d: %s" % (e.args[0],e.args[1])


#将用户信息保存到数据库person_info表中函数
def save_person_info(uid,name,sex,common,fans_num):
    count = cur.execute('select * from person_info where uid = %s',uid)
    if count == 0:
        values = [uid,name,sex,common,fans_num]
        cur.execute('insert into person_info(uid,name,sex,common,fans_num) values(%s,%s,%s,%s,%s)',values)

#将微博信息保存到数据库person_weibo表中函数
def save_person_weibo(bid,uid,body,create_time):
    count = cur.execute('select * from person_weibo where body = %s',body)
    if count == 0:
        values = [bid,uid,body,create_time]
        cur.execute('insert into person_weibo(bid,uid,body,create_time) values(%s,%s,%s,%s)',values)


if __name__ == "__main__":
    weibo = WeiBo()
    weibo.login('13580473454','19921023')

#count = cur.execute('select * from person_info')
#print 'count = ' + str(count)
##登录微博
#login_weibo()
#save_person_info(1944103663,'姚敦鼎','男','无',218)
#conn.commit()
#cur.execute('select id from person_info where uid = (select uid from person_weibo where id = (select max(id) from person_weibo));')
#print '初始化数据库·····'
##从上一次搜的人接着搜
#id = cur.fetchone()[0]
#print 'init_id = ' + str(id)
#while (1):
#    #从数据库中获取到uid进行爬虫
##    dictCur = conn.cursor(MySQLdb.cursors.DictCursor)
#    cur.execute('select uid from person_info where id = %s',id)
#    user_uid = cur.fetchone()[0]
#    cur.execute('select name from person_info where id = %s',id)
#    user_name = cur.fetchone()[0]
#    #爬微博
#    creep_weibo(user_uid)
#    #从关注人列表中爬
#    creep_follows(user_uid)
#    id = id + 1
#conn.close()
