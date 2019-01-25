#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Subjects using prepared statements

Example:
	cur.execute(read, (153,))

SQL-Statement   Paramters
--------------------------------------
create          Name, Short, Advanced
listing			-
search			Name
read			Rowid
update          Name, Short, Advanced, Rowid
delete          Rowid
"""

__author__ = "Christian Glöckner"

setup = """create table Subjects (
	name varchar(25) not null,
	short varchar(5) not null,
	advanced tinyint check (advanced in (0, 1))
);"""

create  = "insert into Subjects (name, short, advanced) values (?, ?, ?)"
listing = "select rowid from Subjects"
search  = "select rowid from Subjects where name like ?"
read    = "select name, short, advanced from Subjects where rowid = ?"
update  = "update Subjects set name = ?, short = ?, advanced = ? where rowid = ?"
delete  = "delete from Subjects where rowid = ?"

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

	def test_create_listing_destroy(self):
		# create records
		self.cur.executemany(create, [
			('maths', 'Ma', 1,),
			('chemistry', 'che', None,),
			('english', 'eng', 0,)
		])
		self.db.commit()
		
		# list
		self.cur.execute(listing)
		ids = self.cur.fetchall()
		self.assertEqual(ids, [(1,), (2,), (3,),])
		
		# destroy records
		self.cur.executemany(delete, [
			(1,),
			(2,),
			(3,) 
		])
		self.db.commit()
	
	def test_search_read(self):
		# create records
		self.cur.executemany(create, [
			('maths', 'Ma', 1,),
			('chemistry', 'che', None,),
			('english', 'eng', 0,)
		])
		self.db.commit()
		
		# search id by name
		self.cur.execute(search, ('%mist%',))
		id = self.cur.fetchall()
		self.assertEqual(id, [(2,)])
		
		# read data by id
		self.cur.execute(read, (1,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('maths', 'Ma', 1,)])

	def test_update(self):
		# create records
		self.cur.executemany(create, [
			('maths', 'Ma', 1,),
			('chemistry', 'che', None,),
			('english', 'eng', 0,)
		])
		self.db.commit()
		
		# update data
		self.cur.execute(update, ('biology', 'bio', 0, 2,))
		self.db.commit()
		
		# assert update
		self.cur.execute(read, (2,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('biology', 'bio', 0,)])

if __name__ == '__main__':
	unittest.main()

