#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Subjects using prepared statements

Example:
	cur.execute(readNameById, (153,))

SQL-Statement   Paramters
-------------------------	
create          Name
readNameById    Rowid
readIdByName    Name
update          Name, Rowid
delete          Rowid
"""

__author__ = "Christian Glöckner"

setup = """create table Subjects (
	name varchar(25) unique
);"""

create = "insert into Subjects (name) values (?)"

readNameById = "select name from Subjects where rowid = ?"
readIdByName = "select rowid from Subjects where name = ?"

update = "update Subjects set name = ? where rowid = ?"

delete = "delete from Subjects where rowid = ?"

# -----------------------------------------------------------------------------

import sqlite3, unittest

class CRUDTest(unittest.TestCase):

	def setUp(self):
		# create empty database
		self.db  = sqlite3.connect('')
		self.cur = self.db.cursor()
		# setup tables
		self.cur.execute(setup)
		self.db.commit()
	
	def tearDown(self):
		# reset database
		self.db = None

	def test_lifecycle(self):
		# create records
		self.cur.executemany(create, [
			('maths',),
			('chemistry',),
			('english',)
		])
		self.db.commit()
		
		# read
		self.cur.execute(readIdByName, ('chemistry',))
		result = self.cur.fetchall()
		self.assertEqual(len(result), 1)
		
		# destroy records
		self.cur.executemany(delete, [
			(1,),
			(2,),
			(3,) 
		])
		self.db.commit()
	
	def test_uniqueNames(self):
		# create records
		self.cur.executemany(create, [
			('maths',),
			('chemistry',),
			('english',)
		])
		self.db.commit()
		
		# force duplicates
		with self.assertRaises(sqlite3.IntegrityError):
			self.cur.execute(create, ('chemistry',),)
	
	def test_readRecords(self):
		# create records
		self.cur.executemany(create, [
			('maths',),
			('chemistry',),
			('english',)
		])
		self.db.commit()
		
		# read id by name
		self.cur.execute(readIdByName, ('chemistry',))
		id = self.cur.fetchall()
		self.assertEqual(id, [(2,)])
		
		# read name by id
		self.cur.execute(readNameById, (1,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('maths',)])

if __name__ == '__main__':
	unittest.main()

