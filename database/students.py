#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Students	 using prepared statements

SQL-Statement   Paramters
-------------------------------------
create          Surname, FirstName, ClassId, PersonId 
listing			-
search			Surname, FirstName
lookup			ClassId
derive			PersonId
read			Rowid
rename          Surname, FirstName
move			ClassId
delete          Rowid
"""

__author__ = "Christian Glöckner"

setup = """create table Students (
	surname varchar(25) not null,
	first_name varchar(25) not null,
	class_id int,
	person_id int unique,
	foreign key (class_id) references Classes(rowid),
	foreign key (person_id) references Persons(rowid)
);"""

create  = "insert into Students (surname, first_name, class_id, person_id) values (?, ?, ?, ?)"
listing = "select rowid from Students"
search  = "select rowid from Students where surname like ? or first_name like ?"
lookup  = "select rowid from Students where class_id = ?"
derive  = "select rowid from Students where person_id = ?"
read    = "select surname, first_name, Classes.form, Classes.short, Teachers.Short from Students left join Classes on Students.class_id = Classes.rowid left join Teachers on Classes.teacher_id = Teachers.rowid where Students.rowid = ?"
rename  = "update Students set surname = ?, first_name = ? where rowid = ?"
move    = "update Students set class_id = ? where rowid = ?"
delete  = "delete from Students where rowid = ?"

# -----------------------------------------------------------------------------

import sqlite3, unittest

class CRUDTest(unittest.TestCase):

	def setUp(self):
		from database import persons, teachers, classes
	
		# create empty database
		self.db  = sqlite3.connect('')
		self.cur = self.db.cursor()
		# setup tables
		self.cur.execute(persons.setup)
		self.cur.execute(teachers.setup)
		self.cur.execute(classes.setup)
		self.cur.execute(setup)
		self.cur.executemany(persons.create, [(), (), (), (), ()])
		self.cur.executemany(teachers.create, [
			('Foo', 'f', 'FO', 1,),
			('Bar', 'm', 'BA', 2,)
		])
		self.cur.executemany(classes.create, [
			(10, 'b', None,),
			(8, 'a', 2,)
		])
		self.db.commit()
	
	def tearDown(self):
		# reset database
		self.db = None

	def test_create_listing_delete(self):
		# create records
		# create records
		self.cur.executemany(create, [
			('Mustermann', 'Max', 2, 3, ),
			('Bleistift', 'Sandra', None, 4, ),
			('Doe', 'John', 2, 5, )
		])
		self.db.commit()
		
		# list
		self.cur.execute(listing)
		ids = self.cur.fetchall()
		self.assertEqual(set(ids), set([(1,), (2,), (3,)]))
		
		# destroy records
		self.cur.executemany(delete, [
			(1,),
			(2,)
		])
		self.db.commit()

	def test_search_read(self):
		# create records
		self.cur.executemany(create, [
			('Mustermann', 'Max', 2, 3, ),
			('Bleistift', 'Sandra', None, 4, ),
			('Doe', 'John', 2, 5, )
		])
		self.db.commit()
		
		# TODO: search by classID (expect two students)
		# TODO: search by personID (expect one student)
		"""
		# search id by 
		self.cur.execute(search, (8, '%st%',))
		id = self.cur.fetchall()
		self.assertEqual(id, [(2,)])
		"""
		
		# read data by id
		self.cur.execute(read, (1,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('Mustermann', 'Max', 8, 'a', 'BA',)])

	def test_rename(self):
		# create records
		self.cur.executemany(create, [
			('Mustermann', 'Max', 2, 3, ),
			('Bleistift', 'Sandra', None, 4, ),
			('Doe', 'John', 2, 5, )
		])
		self.db.commit()
		
		# update data
		self.cur.execute(rename, ('Smith', 'Jane', 3,))
		self.db.commit()
		
		# assert rename
		self.cur.execute(read, (3,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('Smith', 'Jane', 8, 'a', 'BA')])

	def test_move(self):
		# create records
		self.cur.executemany(create, [
			('Mustermann', 'Max', 2, 3, ),
			('Bleistift', 'Sandra', None, 4, ),
			('Doe', 'John', 2, 5, )
		])
		self.db.commit()
		
		# update data
		self.cur.execute(move, (1, 3,))
		self.db.commit()
		
		# assert move
		self.cur.execute(read, (3,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('Doe', 'John', 10, 'b', None)])

		# update data
		self.cur.execute(move, (None, 3,))
		self.db.commit()
		
		# assert move
		self.cur.execute(read, (3,))
		name = self.cur.fetchall()
		self.assertEqual(name, [('Doe', 'John', None, None, None)])
