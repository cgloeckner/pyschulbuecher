#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Persons using prepared statements

Note that the persons' table is only used for hierarchic structuring. Pure
persons only be created and deleted. Other data is added by additional tables
which provide role-specific data.

SQL-Statement   Paramters
-------------------------	
create          -
delete          Rowid
"""

__author__ = "Christian Glöckner"

# note: stub is only a placeholder
setup = """create table Persons (
	stub tinyint
);"""

create = "insert into Persons values (0)"

delete = "delete from Persons where rowid = ?"

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
		self.cur.executemany(create, [(), (), ()])
		self.db.commit()
		
		# read
		self.cur.execute("select rowid from Persons")
		ids = self.cur.fetchall()
		self.assertEqual(ids, [(1,), (2,), (3,),])
		
		# destroy records
		self.cur.executemany(delete, [
			(1,),
			(2,),
			(3,) 
		])
		self.db.commit()

if __name__ == '__main__':
	unittest.main()

