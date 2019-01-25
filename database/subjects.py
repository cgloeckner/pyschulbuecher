#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Subjects using prepared statements

Example:
	cur.execute(read('*', 'rowid'), (153,))

SQL-Statement   Paramters
--------------------------------------
create          Name, Short, Advanced
read(fetch,by)	corresponding to `by`
update          Name, Rowid
delete          Rowid
"""

__author__ = "Christian Glöckner"

setup = """create table Subjects (
	name varchar(25) not null,
	short varchar(5) not null,
	advanced tinyint check (advanced in (0, 1))
);"""

create = "insert into Subjects (name, short, advanced) values (?, ?, ?)"

def read(fetch, by):
	"""read(fetch, by)
	
	e.g. read('*', 'rowid')
	
	Provide an SQL statement for selecting the columns `fetch` by the column
	value of `by`. NEVER let `fetch` or `by` be input strings - use hardcoded
	string literals only to AVOID SQL INJECTIONS."""
	return "select {0} from Subjects where {1} = ?".format(fetch, by)

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
			('maths', 'Ma', 1,),
			('chemistry', 'che', None,),
			('english', 'eng', 0,)
		])
		self.db.commit()
		
		# read
		self.cur.execute(read('rowid', 'name'), ('chemistry',))
		result = self.cur.fetchall()
		self.assertEqual(len(result), 1)
		
		# destroy records
		self.cur.executemany(delete, [
			(1,),
			(2,),
			(3,) 
		])
		self.db.commit()
	
	def test_readRecords(self):
		# create records
		self.cur.executemany(create, [
			('maths', 'Ma', 1,),
			('chemistry', 'che', None,),
			('english', 'eng', 0,)
		])
		self.db.commit()
		
		# read id by name
		self.cur.execute(read('rowid', 'name'), ('chemistry',))
		id = self.cur.fetchall()
		self.assertEqual(id, [(2,)])
		
		# read multiple data by id
		self.cur.execute(read('name, short', 'rowid'), (1,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('maths', 'Ma',)])
		
		# read all data by id
		self.cur.execute(read('*', 'rowid'), (1,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('maths', 'Ma', 1,)])

if __name__ == '__main__':
	unittest.main()

