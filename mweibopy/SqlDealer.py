#coding = UTF-8

import MySQLdb

class Queue:
	def __init__(self):
		self.queue = []
		self.front = 0
		self.rear = 1
	
	def pop(self):
		if front < rear:
			v =  self.queue[self.front]
			self.front++
			return v
		else :
			return None
	
	def push(self,data):
		self.queue[self.rear] = data
		self.rear++
		pass
	
	def lenof(self):
		return self.rear - self.front - 1

class SqlDealer:
	def __init__(self,dbname):
		try:
			self.dbname = dbname
			self.conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db=self.dbname,port=3306)
			self.cur=conn.cursor()
			self.cur.execute('select * from user')
			self.cur.close()
			self.conn.close()
		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
			return -1
		self.insertqueue = Queue()

	def addToInsertQueue(self.data,dataTable,sqlstr):
		self.insertqueue.append({
			data : data,
			dataTable : dataTable,
			sqlstr : sqlstr
		})	
	
	def dealTheInsertQueue(self):
		v = self.insertqueue.pop()
		if v != None:
			self.cur.excute(v['sqlstr'],v.data)
			self.conn.commit()	
	
	def closeConn(self):
		try:
			self.conn.close()
		except MySQLdb.Error,e:
			print 'mysql error'
	


