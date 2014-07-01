# coding = UTF-8

import re
import json

ss = str('');
with open('test','r') as f:
	for line in f.readlines():
		ss += line
dd = unicode(json.loads(ss))
#print unicode(dd)

restr = r'<div .*?class="WB_feed_type.*?>.*?<div class="WB_screen.*?>.*?<div.*?class="WB_text.*?>.*?<div.*?class="WB_func.*?></div.*?>.*?</div>'
#restr = r"\\n"
temp = r'<div .*?class=\"WE_feed_type.*?>.*?<div'
weibo = re.compile(restr)
arr = weibo.findall(dd)
forward = 0
for i in arr:
	#print i

	#whether forward
	restr = r'isForward'
	isForward = re.compile(restr)
	restr = r'tbinfo'
	isRight = re.compile(restr)
	rs = isForward.search(i)
	rss = isRight.search(i)
	if  rs != None:
		forward += 1 
		continue
	if  rss == None:
		forward += 1
		continue
	#fetch name
	restr = r'<div class="WB_info">.*?title="(.*?)".*?usercard="id=(.*?)"'
	nameanduid = re.compile(restr)
	rs = nameanduid.search(i)
	print unicode(rs.group(1).decode('unicode-escape')) + ' ' + rs.group(2) 
	name = rs.group(1).decode('unicode-escape')
	uid  = rs.group(2)
	
	#fetch neirong
	restr = r'<div class="WB_text".*?>(.*?)</div>'	
	content = re.compile(restr)
	rs = content.search(i)
	content_str = rs.group(1).decode('unicode-escape')
	print rs.group(1).decode('unicode-escape')
	

	#fetch date
	restr = r'<div.*?date="(.*?)".*?WB_time'
	timestamp = re.compile(restr)
	rs = timestamp.search(i)
	timestamp_str = (rs.group(1)[:-2])
        print 'timestamp '+timestamp_str	
	#fetch url
        restr = r'WB_from.*?<a.*?href="(.*?)\?'
        url = re.compile(restr)
        rs = url.search(i)
        url_str = rs.group(1)
        print 'URL : '+url_str
	#fetch weibo_id
        restr = r' mid="(.*?)"'
        mid = re.compile(restr)
        rs = mid.search(i)
        mid_str = rs.group(1)
        print "mid : " + mid_str
    
	print '\n\n'
        
print forward

#uni = unicode('\u5b89\u5353\u8bba\u575b','utf-8')
#uni = uni.decode('unicode-escape')
#print uni

#print weibo.group()
#print dd
print len(arr)


print time.clock()
