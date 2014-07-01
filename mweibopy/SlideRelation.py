# coding=UTF-8

import re
import json
import SlideBase
import RelationshipConfig
import time
import logging
import os

from mypachongweibo import *
from globalConfig import *
from SqlDealer import *
from timer import *

with open('test2','r') as f:
	ss = ''
	for line in f.readlines():
		ss += line
#print ss


class SlideRelation(SlideBase.SlideBase):

	def __init__(self,text,sqldealer):
		self.text = text
		self.sqldealer = sqldealer
	
	def run(self,suid):
		try:
			suid = long(suid)
			restr = r'cnfList.*?</script>'
			fetch_html = re.compile(restr,re.DOTALL)
			content = fetch_html.search(self.text).group()
			#print content
			restr = r'<li.*?uid=(.*?)&fnick=(.*?)&.*?>(.*?)<\\/li>'
			split_pattern = re.compile(restr,re.DOTALL)
			follow_str = r'/follow\\".*?>(.*?)<'
			#r'/follow(.*?)>'#
			follow_pattern = re.compile(follow_str,re.DOTALL)
			fan_str = r'/fans\\".*?>(.*?)<'
			fan_pattern = re.compile(fan_str,re.DOTALL)
			arr = split_pattern.findall(content)
			#print len(arr)
			dataTable = "relationship"
			#print arr[0]
			for item in arr:
				try:
					#print item
					uid = long(item[0])
					username = item[1]	
					#print "uid " ,
					#print uid ,
					#print " username ",
					#print username
					sss = "uid " + str(uid) + " username " + username
					logging.debug(sss)
					s = "Insert into relationship VALUES('','%s','%s') " 
					data = [uid,suid]
					self.sqldealer.addToQueue(list(data),dataTable,s)
					follow_rs = follow_pattern.search(item[2])
					follow_num = long(follow_rs.group(1))
					fan_rs = fan_pattern.search(item[2])
					fan_num = long(fan_rs.group(1))
					s = "Insert Into usertable VALUES('',%s,'%s','%s','%s','','0','0') "
					data = [username,uid,follow_num,fan_num]
					self.sqldealer.addToQueue(list(data),"usertable",s)
				except Exception,e:
					print e
					continue

		except Exception,e:
			#something error during sliding
			print e
			logging.error(str(e))
			return -1
		return 1;

class SlideRelationArranger(SlideBase.SlideBaseArranger):

	def __init__(self,text):
		self.dealer = SqlDealer('SlideWeibo')
		self.fail_num = 0

	def runTask(self,suid):
		baseUrl = "http://weibo.com/uid/follow"
		uid = suid
		weibo = WebWeiboSlider()
		#login
		weibo.login('13580473454','19921023')
		opener = weibo.getOpener()
		header = weibo.getHeader()
		
		print "start slide"
		# 逻辑，遍历十页取关注。
		while True:
			sqlstr = "Select uid from userTable where isSlideRelation = '0'"
			rs = self.dealer.select(sqlstr,(),1)
			if rs != None:
				uid = str(rs[0]);	
				print uid,
				print type(uid)
			else :
				print "Slide END"
				break
			slideRelation = SlideRelation("",self.dealer)
			s = baseUrl.replace("uid",uid)
			for i in range(10):
				page = i + 1
				ss = s + "?page="+str(page)
				req = urllib2.Request(ss,headers = header)
				res = -1
				while True:
					try:
						res = self.load(opener,req ,timeout = 10)
						print res
						if res == -1:
							continue
						break
					except Exception,e: 	
						print e
						time.sleep(5)
						continue
				text = res.read()
				slideRelation.text = text
				rs = slideRelation.run(uid)
				if rs != 1:
					break
			sqlstr = "UPDATE userTable SET isSlideRelation = '1' where uid= %s "
			data = [uid]
			self.dealer.executenow(sqlstr,list(data))
				
	def load(self,opener,req,timeout):
		while True:
			try:
				res = opener.open(req,timeout = timeout);
				break
			except Exception,e:
				time.sleep(5)
				continue	
		return res

	def runSqlTask(self): 
		rs = self.dealer.dealTheQueue()
		if rs == 1:
			self.fail_num = 0
			print "success"
		else:
			time.sleep(5)
			self.fail_num += 1
			print "failed"	
			
		#print "run sql task"
		


if __name__ == "__main__":
	logfilename = ""
	logging.basicConfig(filename = os.path.join(os.getcwd(), 'sliderelation_log.txt'), level = logging.DEBUG)
	start_uid = RelationshipConfig.d["startpoint"]
	slide = SlideRelationArranger("")
	# 黑魔法啊黑魔法，等待重构这一段。
	def timertask():
		global slider
		slide.runSqlTask()

	timer = Timer(timertask,(),0.1,False)
	timer.start()
	slide.runTask(start_uid)
	while True:
		time.sleep(20)


