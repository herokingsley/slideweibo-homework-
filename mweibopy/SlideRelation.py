# coding = UTF-8

import re
import json
import SlideBase
from globalConfig import *

with open('test2','r') as f:
	ss = ''
	for line in f.readlines():
		ss += line
#print ss

restr = r'cnfList.*?</script>'
fetch_html = re.compile(restr,re.DOTALL)
content = fetch_html.search(ss).group()
print content
restr = r'<li.*?uid=(.*?)&fnick=(.*?)&.*?>(.*?)<\\/li>'
split_pattern = re.compile(restr,re.DOTALL)
arr = split_pattern.findall(content)
print len(arr)


class SlideRelation(SlideBase.SlideBase):
	def __init__(self,text):
		pass
	pass

class SlideRelationArranger(SlideBase.SlideBaseArranger):
	def __init__(self,text):
		pass
	pass



