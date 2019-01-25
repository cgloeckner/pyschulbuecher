#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Publishers using prepared statements

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

setup = """create table Publishers (
	name varchar(25) unique
);"""

create = "insert into Publishers (name) values (?)"

readNameById = "select name from Publishers where rowid = ?"
readIdByName = "select rowid from Publishers where name = ?"

update = "update Publishers set name = ? where rowid = ?"

delete = "delete from Publishers where rowid = ?"

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
			('Cornelsen',),
			('Klett',),
			('Westermann',)
		])
		self.db.commit()
		
		# read
		self.cur.execute(readIdByName, ('Klett',))
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
			('Cornelsen',),
			('Klett',),
			('Westermann',)
		])
		self.db.commit()
		
		# force duplicates
		with self.assertRaises(sqlite3.IntegrityError):
			self.cur.execute(create, ('Klett',),)
	
	def test_readRecords(self):
		# create records
		self.cur.executemany(create, [
			('Cornelsen',),
			('Klett',),
			('Westermann',)
		])
		self.db.commit()
		
		# read id by name
		self.cur.execute(readIdByName, ('Klett',))
		id = self.cur.fetchall()
		self.assertEqual(id, [(2,)])
		
		# read name by id
		self.cur.execute(readNameById, (1,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('Cornelsen',)])

if __name__ == '__main__':
	unittest.main()

