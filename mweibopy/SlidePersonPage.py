#coding = UTF-8

import re
import json
import SlideBase
import logging
import os
import time
import random

from timer import *
from mypachongweibo import *
from SqlDealer import *

ss = str('');
with open('test','r') as f:
	for line in f.readlines():
		ss += line
dd = json.loads(ss)
text=dd["data"]
#print ss
#print unicode(text)
restr = r''



class SlidePersonPageArranger(SlideBase.SlideBaseArranger):

    def __init__(self,text):
	self.dealer = SqlDealer('SlideWeibo')
	self.fail_num = 0
	
    def runTask(self):
	baseUrl = "http://weibo.com/aj/mblog/mbloglist?count=15&"
	weibo = WebWeiboSlider()
	#login
        weibo.login('410638015@qq.com','weibo19921023')
	#weibo.login('13580473454','19921023')
       # weibo.login('ez_wzr_homework@163.com','19921023')
        opener = weibo.getOpener()
	header = weibo.getHeader()

	print 'start slide'
	while True:
            print "new uid start"
            sqlstr = "select count(*) from userTable where isSlide = '0'"
            rs = self.dealer.select(sqlstr,(),1)
            cc = int(rs[0])
            r = random.randint(0,cc-1)

	    sqlstr = "Select uid,username from userTable where isSlide = '0' LIMIT " + str(r) + " , 1 "
	    rs = self.dealer.select(sqlstr,(),1)
	    if rs != None:
		uid = str(rs[0])
                print uid
		username = unicode(rs[1])
	    else:
		print "Slide End"
		break
	    slidePersonPage = SlidePersonPage("",self.dealer)
	    s = str(baseUrl)
	    s += "uid=" + uid;
            num = 0
	    for i in range(10):
		page = i + 1
		pre_page = page - 1
		if page == 1:
		    pre_page = 1
		for j in range(3):
                    try:
                        pass
                        #time.sleep(5)
                    except Exception,e:
                        pass
		    ss = str(s)
		    #print "j " + str(j)
		    ss += "&pagebar=" + str(j)
		    if page > 1 or j != 0:
			ss += "&pre_page=" + str(pre_page) + "&page=" + str(page)	
		    else:
			ss += "&page=" + str(page)
		    print "url: " + ss
		    req = urllib2.Request(ss,headers = header)	
		    res = -1
		    while True:
                        print "try to load"
			try :
			    res = self.load(opener,req,timeout = 10)
			    if res == -1:
				continue
			    break
		        except Exception,e:
			    print e
			    #time.sleep(5)
			    continue

		    text = res.read()
                    print "load finish"
                    #print text
		    slidePersonPage.text = text
		    rs = slidePersonPage.execute(username,uid)
		    if rs != 1:
		        break
                    else:
                        num += 1
            if num <= 10:
                continue
	    timedate = time.time()
	    sqlstr = "UPDATE userTable SET isSlide = '1',last_slide="+ str(timedate)
	    sqlstr += " where uid = %s" 
	    data = [uid]
	    self.dealer.executenow(sqlstr,list(data))

    def load(self,opener,req,timeout):

        while True:
            try:
                res = opener.open(req,timeout = timeout);
                break
            except Exception,e:
                time.sleep(3)
                continue	
        return res
	
    def runSqlTask(self):
        rs = self.dealer.dealTheQueue()
        if rs == 1:
            self.fail_num = 0
            print "success"
        else:
            time.sleep(0.2)
            self.fail_num += 1
            print "failed"
    
class SlidePersonPage(SlideBase.SlideBase):

    def __init__(self,text,dealer):
	self.text = text
	self.sqldealer = dealer
        #split_pattern = r'<div.*?class="WB_feed_type.*?>.*?<'
        split_pattern = r'<div .*?class="WB_feed_type.*?>.*?<div.*?class="WB_screen.*?>.*?<div.*?class="WB_text.*?>.*?<div.*?class="WB_func.*?></div>.*?</div>'
        self.split_rec = re.compile(split_pattern,re.DOTALL)		
        isForward_pattern = r'isForward'
        self.isForward_rec = re.compile(isForward_pattern,re.DOTALL)

        isOtherForward_pattern = r'tbinfo'
        self.isOtherForward_rec = re.compile(isOtherForward_pattern)
        #needn't to get username and uid
        #nameanduid_pattern = r'<div.*?class="WB_info">.*?title="(.*?)".*?usercard="id=(.*?)"'
        #self.nameanduid_re= re.compile(nameanduid_pattern,re.DOTALL)
            
        content_pattern = r'<div class="WB_text".*?>(.*?)</div>'	
        self.content_rec = re.compile(content_pattern,re.DOTALL)

        #datenum_pattern = r'<div.*?date="(.*?)".*?WB_time'
        datenum_pattern = r'date="(.*?)"'
            
        self.datenum_rec = re.compile(datenum_pattern,re.DOTALL)
            
        url_pattern = r'WB_from.*?<a.*?href="(.*?)[?"]'
        self.url_rec = re.compile(url_pattern,re.DOTALL)

        mid_pattern = r' mid="(.*?)"'
        self.mid_rec = re.compile(mid_pattern,re.DOTALL)
    
    def execute(self,username,uid):
        #self.startExecute()
        #customize
        try:
            dd = json.loads(self.text)
            text=dd["data"]
            print text
            self.data = self.split_rec.findall(text)		
            print len(self.data)
            for item in self.data:
                #print item 
                #print '\n\n'
                #check and filter whether forward
                isForward_rs = self.isForward_rec.search(item)
                isOtherForward_rs = self.isOtherForward_rec.search(item)
                if  isForward_rs != None: 
                    continue
                if  isOtherForward_rs == None:
                    continue
                #fetch username and uid
                #nameanduid_rs = self.nameanduid_rec.search(item)
                #username = nameanduid_rs.group(1).decode('unicode-escape')
                #uid  = nameanduid_rs.group(2)
                #if SlideBase.debug :
                #print 'Username : ' + username + ' Uid : ' + uid 	
                #fetch content
                content_rs = self.content_rec.search(item)
                content = content_rs.group(1)
                content = self.filter_tags(content)
                if SlideBase.debug:
                    print content 
                #fetch date
                datenum_rs = self.datenum_rec.search(item)
                datenum_str = (datenum_rs.group(1)[:-2])
                if SlideBase.debug:
                    print 'timestamp ' + datenum_str	
                #fetch url
                url_rs = self.url_rec.search(item)
                url_str = url_rs.group(1)
                if SlideBase.debug:
                    print 'URL : '+url_str
                #fetch weibo_id
                mid_rs = self.mid_rec.search(item)
                mid_str = mid_rs.group(1)
                sqlstr = "Insert into weibo_content VALUES('',%s,%s,%s,%s,%s,%s)"		
                data = [mid_str,username,uid,url_str,datenum_str,content]
                #self.sqldealer.addToQueue(list(data),"weibo_content",sqlstr)
                self.sqldealer.executenow(sqlstr,list(data) )
                if SlideBase.debug:
                    print "mid : " + mid_str
                    print '\n' 
        #self.endExecute()
        except Exception,e:
            print e
            return -1
        return 1


    def setNewText(self,newText):
        self.text = newText
    
    def setNewUsernameAndUid(username,uid):
        self.username = username
        self.uid = uid
    
    def filter_tags(self,htmlstr):
        #
        re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) 
        re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
        re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
        re_br=re.compile('<br\s*?/?>')#
        re_h=re.compile('</?\w+[^>]*>')#
        re_comment=re.compile('<!--[^>]*-->')#
        s=re_cdata.sub('',htmlstr)#
        s=re_script.sub('',s) #
        s=re_style.sub('',s)#
        s=re_br.sub('\n',s)#
        s=re_h.sub('',s) #
        s=re_comment.sub('',s)#
        #
        blank_line=re.compile('\n+')
        s=blank_line.sub('\n',s)
        s= self.replaceCharEntity(s)#
        return s

    def replaceCharEntity(self,htmlstr):
        CHAR_ENTITIES={'nbsp':' ','160':' ',
                    'lt':'<','60':'<',
                    'gt':'>','62':'>',
                    'amp':'&','38':'&',
                    'quot':'"','34':'"',}

        re_charEntity=re.compile(r'&#?(?P<name>\w+);')
        sz=re_charEntity.search(htmlstr)
        while sz:
            entity=sz.group()#;
            key=sz.group('name')#
            try:
                htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
                sz=re_charEntity.search(htmlstr)
            except KeyError:
                htmlstr=re_charEntity.sub('',htmlstr,1)
                sz=re_charEntity.search(htmlstr)
        return htmlstr

    def replace(self,s,re_exp,repl_string):
        return re_exp.sub(repl_string,s)

if __name__ == "__main__":
    logfilename = ""
    logging.basicConfig(filename = os.path.join(os.getcwd(), 'sliderpersonalpage_log.txt'),level = logging.DEBUG)
    slide = SlidePersonPageArranger("")
    def timertask():
        global slide
        slide.runSqlTask()

    #timer  = Timer(timertask,(),0.1,False)
    #timer.start()
    slide.runTask()
    #slider = SlidePersonPage("",None)
    #slider.text = text
    #slider.execute("kingssssssss",'3213462074')
