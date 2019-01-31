#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Teachers using prepared statements

SQL-Statement   Paramters
-------------------------------------
create          Name, Sex, Short, PersonId
listing			-
search			Short
derive			PersonId
read			Rowid
update          Name, Sex, Short, Rowid
delete          Rowid
"""

__author__ = "Christian Glöckner"

setup = """create table Teachers (
	name varchar(25) not null,
	sex char check (sex in ('m', 'f')),
	short varchar(4) unique,
	person_id int unique,
	foreign key (person_id) references Persons(rowid)
);"""

create  = "insert into Teachers (name, sex, short, person_id) values (?, ?, ?, ?)"
listing = "select rowid from Teachers"
search  = "select rowid from Teachers where short like ?"
derive  = "select rowid from Teachers where person_id = ?"
read    = "select name, sex, short from Teachers where rowid = ?"
update  = "update Teachers set name = ?, sex = ?, short = ? where rowid = ?"
delete  = "delete from Teachers where rowid = ?"

# -----------------------------------------------------------------------------

import sqlite3, unittest

class CRUDTest(unittest.TestCase):

	def setUp(self):
		from database import persons
	
		# create empty database
		self.db  = sqlite3.connect('')
		self.cur = self.db.cursor()
		# setup tables
		self.cur.execute(persons.setup)
		self.cur.execute(setup)
		self.cur.executemany(persons.create, [(), (), (), ()])
		self.db.commit()
	
	def tearDown(self):
		# reset database
		self.db = None

	def test_create_listing_delete(self):
		# create records
		self.cur.executemany(create, [
			('Smith', 'm', 'smi', 1,),
			('Winterbottom', 'f', 'win', 3,),
			('Undef-ined', None, 'und', 2,)
		])
		self.db.commit()
		
		# list
		self.cur.execute(listing)
		ids = self.cur.fetchall()
		self.assertEqual(set(ids), set([(1,), (2,), (3,),]))
		
		# destroy records
		self.cur.executemany(delete, [
			(1,),
			(2,),
			(3,) 
		])
		self.db.commit()

	def test_uniqueShorts(self):
		# create records
		self.cur.executemany(create, [
			('Smith', 'm', 'smi', 1,),
			('Winterbottom', 'f', 'win', 3,),
			('Undef-ined', None, 'und', 2,)
		])
		self.db.commit()
		
		# force duplicates
		with self.assertRaises(sqlite3.IntegrityError):
			self.cur.execute(create, ('Foo', 'f', 'smi', 4),)
	
	def test_search_read(self):
		# create records
		self.cur.executemany(create, [
			('Smith', 'm', 'smi', 1,),
			('Winterbottom', 'f', 'win', 3,),
			('Undef-ined', None, 'und', 2,)
		])
		self.db.commit()
		
		# search id by name
		self.cur.execute(search, ('%wi%',))
		id = self.cur.fetchall()
		self.assertEqual(id, [(2,)])
		
		# read data by id
		self.cur.execute(read, (1,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('Smith', 'm', 'smi',)])

	def test_update(self):
		# create records
		self.cur.executemany(create, [
			('Smith', 'm', 'smi', 1,),
			('Winterbottom', 'f', 'win', 3,),
			('Undef-ined', None, 'und', 2,)
		])
		self.db.commit()
		
		# update data
		self.cur.execute(update, ('Nobody', 'm', 'nob', 3,))
		self.db.commit()
		
		# assert update
		self.cur.execute(read, (3,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('Nobody', 'm', 'nob',)])
