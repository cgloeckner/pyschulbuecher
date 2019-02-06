#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Teachers using prepared statements

SQL-Statement   Paramters
-------------------------------------
create          Name, Sex, Tag, PersonId
listing			-
search			Tag
derive			PersonId
read			Rowid
update          Name, Sex, Tag, Rowid
delete          Rowid
"""

__author__ = "Christian Glöckner"

setup = """create table Teachers (
	name varchar(25) not null,
	sex char check (sex in ('m', 'f')),
	tag varchar(4) unique,
	person_id int unique,
	foreign key (person_id) references Persons(rowid)
);"""

from typing import Iterable, Dict, List

def create(db, data: Iterable[Dict]):
	"""Create new teacher using the given list of `data` objects.
	Required information are a `name` str and a `tag` str as well as a person_id
	`int`. The optional sex `str` must be 'm' or 'f' (default: None)."""
	# dump data to list of tuples
	args = list()
	for obj in data:
		assert(isinstance(obj['name'], str))
		assert(isinstance(obj['tag'], str))
		assert(isinstance(obj['person_id'], int))
		if 'sex' not in obj:
			obj['sex'] = None
		raw = (obj['name'], obj['sex'], obj['tag'], obj['person_id'], )
		args.append(raw)
		
	# execute query
	sql = "insert into Teachers (name, sex, tag, person_id) values (?, ?, ?, ?)"
	db.executemany(sql, args)


def readAllIds(db) -> List[int]:
	"""Returns a full listing of all teachers rowids."""
	# execute query
	sql = "select rowid from Teachers"
	cursor = db.execute(sql)
	raw = cursor.fetchall()
	
	# parse result
	ids = list()
	for item in raw:
		ids.append(item[0])
	return ids



def readData(db, rowid: int) -> dict:
	"""Returns the given teachers's (specified by `rowid`) name, sex and tag
	data and person_id.
	"""
	# prepare query
	sql = "select name, sex, tag, person_id from Teachers where rowid = ?"
	cursor = db.execute(sql, (rowid, ))
	raw = cursor.fetchone()
	
	# parse result
	data = dict()
	if raw is not None:
		data['name']      = raw[0]
		data['sex']       = raw[1]
		data['tag']       = raw[2]
		data['person_id'] = raw[3]
	return data


def readRowids(db, tag: str) -> List[int]:
	"""Return teachers' rowids specified by its `tag`."""
	criteria = "%" + tag + "%"
	# execute query
	sql = "select rowid from Teachers where tag like ?"
	cursor = db.execute(sql, (criteria, ))
	raw = cursor.fetchall()
	
	# parse result
	ids = list()
	for item in raw:
		ids.append(item[0])
	return ids


def readByPerson(db, person_id: int) -> int:
	"""Return teacher's rowid specified by its `person_id`."""
	# execute query
	sql = "select rowid from Teachers where person_id = ?"
	cursor = db.execute(sql, (criteria, ))
	raw = cursor.fetchall()
	return raw[0][0]


def update(db, rowid: int, name: str, tag: str, sex: str=None):
	"""Update the given teacher (specified by `rowid`) using the given `name`
	and `tag`. Optionally the `sex` can be specified as 'm' or 'f' (default:
	None).
	"""
	# execute query
	sql = "update Teachers set name = ?, sex = ?, tag = ? where rowid = ?"
	db.execute(sql, (name, sex, tag, rowid, ))


def delete(db, rowid: int):
	"""Delete the given teacher (specified by `rowid`)."""
	# execute query
	sql = "delete from Teachers where rowid = ?"
	db.execute(sql, (rowid, ))


# -----------------------------------------------------------------------------

import sqlite3, unittest

class CRUDTest(unittest.TestCase):

	def setUp(self):
		from database import persons
	
		# create empty database
		self.db  = sqlite3.connect('')
		self.cur = self.db.cursor()
		# setup tables
		self.cur.execute("PRAGMA foreign_keys=ON")
		self.cur.execute(persons.setup)
		self.cur.execute(setup)
		for i in range(4):
			persons.create(self.cur)
		self.db.commit()
	
	def tearDown(self):
		# reset database
		self.db = None

	def test_create_list_delete(self):
		create(self.cur, [
			{'name': 'Mustermann', 'sex': 'm', 'tag': 'Mus', 'person_id': 3}, # male teacher
			{'name': 'Musterwas',              'tag': 'Muw', 'person_id': 4}, # unspecified sex
			{'name': 'Musterfrau', 'sex': 'f', 'tag': 'Muf', 'person_id': 1}  # female teacher
		])
		
		ids = readAllIds(self.cur)
		self.assertEqual(set(ids), set([1, 2, 3]))
		
		delete(self.cur, 2)
		
		ids = readAllIds(self.cur)
		self.assertEqual(set(ids), set([1, 3]))

	def test_read_teacher_data(self):
		create(self.cur, [
			{'name': 'Mustermann', 'sex': 'm', 'tag': 'MuMa', 'person_id': 3}, # male teacher
			{'name': 'Musterwas',              'tag': 'MuWa', 'person_id': 4}, # unspecified sex
			{'name': 'Musterfrau', 'sex': 'f', 'tag': 'MuFr', 'person_id': 1} # female teacher
		])
		
		data = readData(self.cur, 3)
		self.assertEqual(data, {'name': 'Musterfrau', 'sex': 'f', 'tag': 'MuFr', 'person_id': 1})
		
		data = readData(self.cur, 1)
		self.assertEqual(data, {'name': 'Mustermann', 'sex': 'm', 'tag': 'MuMa', 'person_id': 3})
		
		data = readData(self.cur, 2)
		self.assertEqual(data, {'name': 'Musterwas', 'sex': None, 'tag': 'MuWa', 'person_id': 4})

	def test_search_teachers(self):
		create(self.cur, [
			{'name': 'Mustermann', 'sex': 'm', 'tag': 'Mus', 'person_id': 3}, # male teacher
			{'name': 'Musterwas',              'tag': 'Muw', 'person_id': 4}, # unspecified sex
			{'name': 'Musterfrau', 'sex': 'f', 'tag': 'Muf', 'person_id': 1} # female teacher
		])
		
		ids = readRowids(self.cur, 'Mu')
		self.assertEqual(set(ids), set([1, 2, 3]))
		
		ids = readRowids(self.cur, 'us')
		self.assertEqual(set(ids), set([1]))
		
		ids = readRowids(self.cur, 'Foo')
		self.assertEqual(set(ids), set([]))
		
	def test_update_teachers(self):
		create(self.cur, [
			{'name': 'Mustermann', 'sex': 'm', 'tag': 'Mus', 'person_id': 3}, # male teacher
			{'name': 'Musterwas',              'tag': 'Muw', 'person_id': 4}, # unspecified sex
			{'name': 'Musterfrau', 'sex': 'f', 'tag': 'Muf', 'person_id': 1} # female teacher
		])
		
		# change given sex
		update(self.cur, 1, 'Meyer', 'Me', sex='f')
		data = readData(self.cur, 1)
		self.assertEqual(data, {'name': 'Meyer', 'sex': 'f', 'tag': 'Me', 'person_id': 3})
		
		# set sex
		update(self.cur, 2, 'Meyer', 'Me2', sex='m')
		data = readData(self.cur, 2)
		self.assertEqual(data, {'name': 'Meyer', 'sex': 'm', 'tag': 'Me2', 'person_id': 4})
		
		# unset sex
		update(self.cur, 3, 'Meyer', 'Me3')
		data = readData(self.cur, 3)
		self.assertEqual(data, {'name': 'Meyer', 'sex': None, 'tag': 'Me3', 'person_id': 1})
	
	def test_unique_tag(self):
		create(self.cur, [
			{'name': 'Mustermann', 'sex': 'm', 'tag': 'Mus', 'person_id': 3}, # male teacher
			{'name': 'Musterwas',              'tag': 'Muw', 'person_id': 4}, # unspecified sex
			{'name': 'Musterfrau', 'sex': 'f', 'tag': 'Muf', 'person_id': 1}  # female teacher
		])
		
		with self.assertRaises(sqlite3.IntegrityError):
			update(self.cur, 2, 'irgendwas', 'Mus')
	
	def test_unique_person(self):
		create(self.cur, [
			{'name': 'Mustermann', 'sex': 'f', 'tag': 'Mus', 'person_id': 2},
		])
		with self.assertRaises(sqlite3.IntegrityError):
			create(self.cur, [
				{'name': 'Mustermann', 'sex': 'f', 'tag': 'Mus', 'person_id': 2},
				{'name': 'Mustermann', 'sex': 'f', 'tag': 'Mu2', 'person_id': 2}
			])

		ids = readAllIds(self.cur)
		self.assertEqual(set(ids), set([1]))

	def test_invalid_sex(self):
		with self.assertRaises(sqlite3.IntegrityError):
			create(self.cur, [
				{'name': 'Mustermann', 'sex': 'n', 'tag': 'Mus', 'person_id': 3}
			])

		ids = readAllIds(self.cur)
		self.assertEqual(set(ids), set())



