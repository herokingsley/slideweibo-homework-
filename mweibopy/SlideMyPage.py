# coding=UTF-8

import re
import json
import SlideBase

ss = str('');
with open('test','r') as f:
	for line in f.readlines():
		ss += line
dd = unicode(json.loads(ss))
#print unicode(dd)

class SlideMyPageArranger(SlideBase.SlideBaseArranger):
	def __init__(self):
           self.urllist = [] 
        def run(self,url='http://www.weibo.com/aj/mblog/fsearch?_wv=5&page=1&count=15&pagebar=0',para,header):
           prepara = {
            _wv : 5
           }  
           para.update(prepara)
            
           self.slidemypage = SlideMyPage() 
            
	

class SlideMyPage(SlideBase.SlideBase):

	def __init__(self,text):
		self.text = text
		split_pattern = r'<div .*?class="WB_feed_type.*?>.*?<div class="WB_screen.*?>.*?<div.*?class="WB_text.*?>.*?<div.*?class="WB_func.*?></div.*?>.*?</div>'
		self.split_rec = re.compile(split_pattern)		
		isForward_pattern = r'isForward'
		self.isForward_rec = re.compile(isForward_pattern)

		isOtherForward_pattern = r'tbinfo'
		self.isOtherForward_rec = re.compile(isOtherForward_pattern)

		#nameanduid_pattern = r'<div class="WB_info">.*?title="'
		nameanduid_pattern = r'<div class="WB_info">.*?title="(.*?)".*?usercard="id=(.*?)"'
		self.nameanduid_rec = re.compile(nameanduid_pattern)
		
		content_pattern = r'<div class="WB_text".*?>(.*?)</div>'	
		self.content_rec = re.compile(content_pattern)

		datenum_pattern = r'<div.*?date="(.*?)".*?WB_time'
		self.datenum_rec = re.compile(datenum_pattern)
		
		url_pattern = r'WB_from.*?<a.*?href="(.*?)\?'
		self.url_rec = re.compile(url_pattern)

		mid_pattern = r' mid="(.*?)"'
		self.mid_rec = re.compile(mid_pattern)
	
	def execute(self):
		self.startExecute()
		#customize
		self.data = self.split_rec.findall(self.text)		
		for item in self.data:
			#check and filter whether forward
			isForward_rs = self.isForward_rec.search(item)
			isOtherForward_rs = self.isOtherForward_rec.search(item)
			if  isForward_rs != None: 
				continue
			if  isOtherForward_rs == None:
				continue
			#fetch username and uid
			nameanduid_rs = self.nameanduid_rec.search(item)
			username = nameanduid_rs.group(1).decode('unicode-escape')
			uid  = nameanduid_rs.group(2)
			if SlideBase.debug :
				print 'Username : ' + username + ' Uid : ' + uid 	
			#fetch content
			content_rs = self.content_rec.search(item)
			content = content_rs.group(1).decode('unicode-escape')
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
			if SlideBase.debug:
				print "mid : " + mid_str
				print '\n' 
		self.endExecute()
		pass

	def setNewText(self,newText):
		self.text = newText
	
	def addToOutPutQueue(self,datarow,table):
		pass

if __name__ == "__main__":
	weibo = SlideMyPage(dd)	
	weibo.execute()
