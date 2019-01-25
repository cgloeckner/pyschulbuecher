#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Classes using prepared statements

SQL-Statement   Paramters
-------------------------------------
create          Form, Short, TeacherId
listing			-
search			Form, Short
read			Rowid
update          Form, Short, TeacherId, Rowid
delete          Rowid
"""

__author__ = "Christian Glöckner"

setup = """create table Classes (
	form int not null,
	short varchar(4) not null,
	teacher_id int,
	foreign key (teacher_id) references Teachers(rowid)
);"""

create  = "insert into Classes (form, short, teacher_id) values (?, ?, ?)"
listing = "select rowid from Classes"
search  = "select rowid from Classes where form = ? and short like ?"
read    = "select form, Classes.short, Teachers.Short from Classes inner join Teachers on Teachers.rowid = Classes.teacher_id where Classes.rowid = ?"
update  = "update Classes set form = ?, short = ?, teacher_id = ? where rowid = ?"
delete  = "delete from Classes where rowid = ?"

# -----------------------------------------------------------------------------

import sqlite3, unittest

class CRUDTest(unittest.TestCase):

	def setUp(self):
		import persons, teachers
	
		# create empty database
		self.db  = sqlite3.connect('')
		self.cur = self.db.cursor()
		# setup tables
		self.cur.execute(persons.setup)
		self.cur.execute(teachers.setup)
		self.cur.execute(setup)
		self.cur.executemany(persons.create, [(), ()])
		self.cur.executemany(teachers.create, [
			('Foo', 'f', 'FO', 1, ),
			('Bar', 'm', 'BA', 2, )
		])
		self.db.commit()
	
	def tearDown(self):
		# reset database
		self.db = None

	def test_create_listing_delete(self):
		# create records
		self.cur.executemany(create, [
			(10, 'b', 2,),
			(8, 'a', 1, )
		])
		self.db.commit()
		
		# list
		self.cur.execute(listing)
		ids = self.cur.fetchall()
		self.assertEqual(set(ids), set([(1,), (2,),]))
		
		# destroy records
		self.cur.executemany(delete, [
			(1,),
			(2,)
		])
		self.db.commit()

	def test_search_read(self):
		# create records
		self.cur.executemany(create, [
			(10, 'b', 2,),
			(8, 'test', 1, )
		])
		self.db.commit()
		
		# search id by form and short
		self.cur.execute(search, (8, '%st%',))
		id = self.cur.fetchall()
		self.assertEqual(id, [(2,)])
		
		# read data by id
		self.cur.execute(read, (1,))
		name = self.cur.fetchall()
		self.assertEqual(name, [(10, 'b', 'BA',)])

	def test_update(self):
		# create records
		self.cur.executemany(create, [
			(10, 'b', 2,),
			(8, 'test', 1, )
		])
		self.db.commit()
		
		# update data
		self.cur.execute(update, (9, 'a', 2, 2,))
		self.db.commit()
		
		# assert update
		self.cur.execute(read, (2,))
		name = self.cur.fetchall()
		self.assertEqual(name, [(9, 'a', 'BA',)])

if __name__ == '__main__':
	unittest.main()

