#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Teachers using prepared statements

SQL-Statement   Paramters
-------------------------	
create          Abrev
readAbrevById   Rowid
readIdByAbrev   Abrev
update          Abrev, Rowid
delete          Rowid
"""

__author__ = "Christian Glöckner"

setup = """create table Teachers (
	abrev varchar(4) unique
);"""

create = "insert into Teachers (abrev) values (?)"

readAbrevById = "select abrev from Teachers where rowid = ?"
readIdByAbrev = "select rowid from Teachers where abrev = ?"

update = "update Teachers set abrev = ? where rowid = ?"

delete = "delete from Teachers where rowid = ?"

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

	# to be implemented

if __name__ == '__main__':
	unittest.main()

