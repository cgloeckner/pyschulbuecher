#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Classes using prepared statements

SQL-Statement   Paramters
-------------------------------------
create          Form, Short, TeacherId
listing			-
search			Form, Tag
read			Rowid
update          Form, Tag, TeacherId, Rowid
delete          Rowid
"""

__author__ = "Christian Glöckner"

setup = """create table Classes (
	form int not null,
	tag varchar(4) not null,
	teacher_id int,
	foreign key (teacher_id) references Teachers(rowid)
		on delete set null
);"""


def create(db, data):
	"""Create new classes using the given list of `data` objects."""
	# dump data to list of tuples
	args = list()
	assert(isinstance(data, list))
	for obj in data:
		assert(isinstance(obj, dict))
		assert(isinstance(obj['form'], int))
		assert(isinstance(obj['tag'], str))
		if 'teacher_id' in obj:
			teacher_id = obj['teacher_id']
			assert(isinstance(obj['teacher_id'], int))
		else:
			teacher_id = None
		raw = (obj['form'], obj['tag'], teacher_id, )
		args.append(raw)
		
	# execute query
	sql = "insert into Classes (form, tag, teacher_id) values (?, ?, ?)"
	db.executemany(sql, args)


def readAllIds(db):
	"""Returns a full listing of all classes ids."""
	# execute query
	sql = "select rowid from Classes"
	cursor = db.execute(sql)
	raw = cursor.fetchall()
	
	# parse result
	ids = list()
	for item in raw:
		ids.append(item[0])
	return ids


def readData(db, rowid):
	"""Returns the following information of the given class (specified by
	`rowid`): form, tag, teacher's tag (if a teacher was assigned)
	"""
	# prepare query
	sql = """select form, Classes.tag, Teachers.tag from Classes
		left join Teachers on Teachers.rowid = Classes.teacher_id
		where Classes.rowid = ?"""
	cursor = db.execute(sql, (rowid, ))
	raw = cursor.fetchone()
	
	# parse result
	data = dict()
	if raw is not None:
		data['form']  = raw[0]
		data['tag'] = raw[1]
		data['teacher_tag'] = raw[2]
	return data


def readRowids(db, form=None, tag=None):
	"""Return classes rowids specified by form and/or tag. At least one is
	required to be not None"""
	# prepare query
	sql   = "select rowid from Classes where "
	where = None
	args  = list()
	if form is not None:
		where = "form = ?"
		args.append(form)
	if tag is not None:
		if where is not None:
			where += " and "
		else:
			where = ""
		where += "tag like ?"
		args.append(tag)
	assert(isinstance(where, str))
	sql += where
	args = tuple(args)
	
	# execute query
	cursor = db.execute(sql, args)
	raw = cursor.fetchall()
	
	# parse result
	ids = list()
	for item in raw:
		ids.append(item[0])
	return ids


def rename(db, rowid, form, tag):
	"""Rename the given class (specified by `rowid`) using `form` and `tag`
	tag."""
	# execute query
	sql = "update Classes set form = ?, tag = ? where rowid = ?"
	db.execute(sql, (form, tag, rowid, ))


def changeTeacher(db, rowid, teacher_id=None):
	"""Change the given class' (specified by `rowid`) `teacher_id`. Not
	specifying a `teacher_id` defaults to setting to no teacher being assigned.
	"""
	# execute query
	sql = "update Classes set teacher_id = ? where rowid = ?"
	db.execute(sql, (teacher_id, rowid, ))


def delete(db, rowid):
	"""Delete the given class (specified by `rowid`)."""
	# execute query
	sql = "delete from Classes where rowid = ?"
	db.execute(sql, (rowid, ))


# -----------------------------------------------------------------------------

import sqlite3, unittest

class CRUDTest(unittest.TestCase):

	def setUp(self):
		from database import persons, teachers
	
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

	def test_create_list_delete(self):
		create(self.cur, [
			{'form': 10, 'tag': 'b', 'teacher_id': 2},
			{'form':  8, 'tag': 'a', 'teacher_id': 1},
			{'form':  7, 'tag': 'c'} # without teacher
		])
		
		ids = readAllIds(self.cur)
		self.assertEqual(set(ids), set([1, 2, 3]))
		
		delete(self.cur, 2)
		
		ids = readAllIds(self.cur)
		self.assertEqual(set(ids), set([1, 3]))

	def test_read_class_data(self):
		create(self.cur, [
			{'form': 10, 'tag': 'b', 'teacher_id': 2},
			{'form':  8, 'tag': 'a', 'teacher_id': 1},
			{'form':  7, 'tag': 'c'}
		])
		
		data = readData(self.cur, 2)
		self.assertEqual(data, { 'form': 8, 'tag': 'a', 'teacher_tag': 'FO' })
		
		data = readData(self.cur, 3)
		self.assertEqual(data, { 'form': 7, 'tag': 'c', 'teacher_tag': None })

		data = readData(self.cur, 123)
		self.assertEqual(data, {})

	def test_search_classes(self):
		create(self.cur, [
			{'form': 10, 'tag': 'b', 'teacher_id': 2},
			{'form': 10, 'tag': 'a', 'teacher_id': 1},
			{'form':  8, 'tag': 'a'}
		])
		
		ids = readRowids(self.cur, form=10)
		self.assertEqual(set(ids), set([1, 2]))
		
		ids = readRowids(self.cur, tag='a')
		self.assertEqual(set(ids), set([2, 3]))
		
		ids = readRowids(self.cur, form=10, tag='a')
		self.assertEqual(set(ids), set([2]))
		
		ids = readRowids(self.cur, form=10, tag='c')
		self.assertEqual(set(ids), set([]))
		
		ids = readRowids(self.cur, form=9, tag='a')
		self.assertEqual(set(ids), set([]))
		
		ids = readRowids(self.cur, tag='c')
		self.assertEqual(set(ids), set([]))
		
		ids = readRowids(self.cur, form=9)
		self.assertEqual(set(ids), set([]))
		
	def test_rename(self):
		create(self.cur, [
			{'form': 10, 'tag': 'b', 'teacher_id': 2},
			{'form':  8, 'tag': 'a', 'teacher_id': 1},
			{'form':  7, 'tag': 'c'}
		])
		
		rename(self.cur, 2, 9, 'b')
		
		data = readData(self.cur, 2)
		self.assertEqual(data, { 'form': 9, 'tag': 'b', 'teacher_tag': 'FO' })
		
		rename(self.cur, 123, 11, 'c') # ignored
		
		data = readData(self.cur, 123)
		self.assertEqual(data, {})
		
	def test_change_teacher(self):
		create(self.cur, [
			{'form': 10, 'tag': 'b', 'teacher_id': 2},
			{'form':  8, 'tag': 'a', 'teacher_id': 1},
			{'form':  7, 'tag': 'c'}
		])
		
		changeTeacher(self.cur, 2, 2)
		
		data = readData(self.cur, 2)
		self.assertEqual(data, { 'form': 8, 'tag': 'a', 'teacher_tag': 'BA' })
		
		changeTeacher(self.cur, 2)
		
		data = readData(self.cur, 2)
		self.assertEqual(data, { 'form': 8, 'tag': 'a', 'teacher_tag': None })
		
		changeTeacher(self.cur, 2, 123) # ignored
		
		data = readData(self.cur, 2)
		self.assertEqual(data, { 'form': 8, 'tag': 'a', 'teacher_tag': None })



