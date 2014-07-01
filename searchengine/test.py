# coding=UTF-8

from sphinxapi import *

cl = SphinxClient() 
cl.Open()
rs = cl.Query('招聘')
print rs
