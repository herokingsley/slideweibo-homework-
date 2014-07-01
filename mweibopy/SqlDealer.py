#coding = UTF-8

import MySQLdb
import logging
import os

class Queue:
	def __init__(self):
		self.queue = []
		self.front = 0
		self.rear = 0
	
	def pop(self):
		if self.front < self.rear:
			v =  self.queue[self.front]
			self.front += 1
			if self.front > 100:
				l = self.len()
				self.queue = self.queue[self.front:self.rear]	
				self.front = 0
				self.rear = l
			return v
		else :
			return None
	
	def push(self,data):
		self.queue.append(data)
		self.rear += 1
		pass
	
	def len(self):
		return self.rear - self.front - 1
	

class SqlDealer:
	def __init__(self,dbname):
		try:
			self.dbname = dbname
			self.conn =MySQLdb.connect(host='localhost',user='root',passwd='888168',db=self.dbname,port=3306,charset='utf8')
			self.cur = self.conn.cursor()
			#self.cur.execute('select * from user')
			#self.cur.close()
			#self.conn.close()
		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
			return -1
		self.queue = Queue()

	def addToQueue(self,data,dataTable,sqlstr):
		#dataTable seems to be useless
		self.queue.push({
			"data" : data,
			"dataTable" : dataTable,
			"sqlstr" : sqlstr
		})	
	
	def dealTheQueue(self):
		v = self.queue.pop()
		if v != None:
			print v["sqlstr"]
			print v["data"]
			#print v["sqlstr"] % v["data"] 
			#for item in v["data"]:
		#    print type(item),
	#    print item
			try :    
				#s = v['sqlstr'] % v['data']
				self.cur.execute(v['sqlstr'],v["data"])
				self.conn.commit()
				logging.debug(v['sqlstr'])
			except Exception,e:
				print e
				logging.error(v['sqlstr'])
				logging.error(str(e))
				return 0
			return 1
		else :
			return -1

	def executenow(self,sqlstr,data):
		try:
			print sqlstr,
			print data
			self.cur.execute(sqlstr,data)
			self.conn.commit()
			print "success"
		except Exception,e:
			print "failed"
			print e

	def select(self,sqlstr,data,returnNum = 1):
		try:
			cur = self.conn.cursor()
			count = cur.execute(sqlstr,data)
			print sqlstr
			if returnNum == 1:
				rs = cur.fetchone();
			elif returnNum < count:
				rs = cur.fetchmany(returnNum)
			else:
				rs = cur.fetchall()
			return rs
		except Exception,e:
			print e
			logging.error(str(e))

	
	def closeConn(self):
		try:
			self.conn.close()
		except MySQLdb.Error,e:
			print 'mysql error'
	


