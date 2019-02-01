#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Persons using prepared statements

Note that the persons' table is only used for hierarchic structuring. Pure
persons only be created and deleted. Other data is added by additional tables
which provide role-specific data.
"""

__author__ = "Christian Glöckner"

# note: stub is only a placeholder
setup = """create table Persons (
	stub tinyint
);"""

from typing import List

def create(db):
	"""Create a new person."""
	# execute query
	sql = "insert into Persons values (0)"
	db.execute(sql)


def readAllIds(db) -> List[int]:
	"""Returns a full listing of all persons ids."""
	# execute query
	sql = "select rowid from Persons"
	cursor = db.execute(sql)
	raw = cursor.fetchall()
	
	# parse result
	ids = list()
	for item in raw:
		ids.append(item[0])
	return ids


def delete(db, rowid: int):
	"""Delete the given person (specified by `rowid`)."""
	# execute query
	sql = "delete from Persons where rowid = ?"
	db.execute(sql, (rowid, ))

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

	def test_create_list_delete(self):
		for i in range(3):
			create(self.cur)
		
		ids = readAllIds(self.cur)
		self.assertEqual(set(ids), set([1, 2, 3]))
		
		delete(self.cur, 2)
		
		ids = readAllIds(self.cur)
		self.assertEqual(set(ids), set([1, 3]))


