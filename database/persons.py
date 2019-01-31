#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Persons using prepared statements

Note that the persons' table is only used for hierarchic structuring. Pure
persons only be created and deleted. Other data is added by additional tables
which provide role-specific data.

SQL-Statement   Paramters
-------------------------	
create          -
listing			-
delete          Rowid
"""

__author__ = "Christian Glöckner"

# note: stub is only a placeholder
setup = """create table Persons (
	stub tinyint
);"""

create  = "insert into Persons values (0)"
listing = "select rowid from Persons"
delete  = "delete from Persons where rowid = ?"

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

	def test_create_listing_delete(self):
		# create records
		self.cur.executemany(create, [(), (), ()])
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

