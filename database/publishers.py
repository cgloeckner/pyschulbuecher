#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Publishers using prepared statements

Example:
	cur.execute(read, (153,))

SQL-Statement   Paramters
-------------------------	
create          Name
search			Name
read            Rowid
update          Name, Rowid
delete          Rowid
"""

__author__ = "Christian Glöckner"

setup = """create table Publishers (
	name varchar(25) unique
);"""

create = "insert into Publishers (name) values (?)"
search = "select rowid from Publishers where name like ?"
read   = "select name from Publishers where rowid = ?"
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

	def test_create_delete(self):
		# create records
		self.cur.executemany(create, [
			('Cornelsen',),
			('Klett',),
			('Westermann',)
		])
		self.db.commit()
		
		# read
		self.cur.execute(read, ('3',))
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
	
	def test_search_read(self):
		# create records
		self.cur.executemany(create, [
			('Cornelsen',),
			('Klett',),
			('Westermann',)
		])
		self.db.commit()
		
		# search id by name
		self.cur.execute(search, ('%kle%',))
		id = self.cur.fetchall()
		self.assertEqual(id, [(2,)])
		
		# read data by id
		self.cur.execute(read, (1,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('Cornelsen',)])

	def test_update(self):
		# create records
		self.cur.executemany(create, [
			('Cornelsen',),
			('Klett',),
			('Westermann',)
		])
		self.db.commit()
		
		# update data
		self.cur.execute(update, ('Spam', 1,))
		
		# assert update
		self.cur.execute(read, (1,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('Spam',)])

if __name__ == '__main__':
	unittest.main()

