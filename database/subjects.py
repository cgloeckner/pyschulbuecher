#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Subjects using prepared statements
"""

__author__ = "Christian Glöckner"

setup = """create table Subjects (
	name varchar(25) not null,
	tag varchar(5) not null,
	advanced tinyint check (advanced in (0, 1))
);"""

from typing import Iterable, Dict, List

def create(db, data: Iterable[Dict]):
	"""Create new subjects using the given list of `data` objects.
	Required information are a `name` str and a `tag` str. An optional
	`advanced` bool can be specified."""
	# dump data to list of tuples
	args = list()
	for obj in data:
		assert(isinstance(obj['name'], str))
		assert(isinstance(obj['tag'], str))
		if 'advanced' in obj:
			advanced = obj['advanced']	
			assert(isinstance(advanced, bool))
			advanced = int(advanced)
		else:
			advanced = None
		raw = (obj['name'], obj['tag'], advanced, )
		args.append(raw)
		
	# execute query
	sql = "insert into Subjects (name, tag, advanced) values (?, ?, ?)"
	db.executemany(sql, args)


def readAllIds(db) -> List[int]:
	"""Returns a full listing of all subject rowids."""
	# execute query
	sql = "select rowid from Subjects"
	cursor = db.execute(sql)
	raw = cursor.fetchall()
	
	# parse result
	ids = list()
	for item in raw:
		ids.append(item[0])
	return ids


def readData(db, rowid: int) -> dict:
	"""Returns the given subject's (specified by `rowid`) name and tag data,
	as well whether it's advanced or not (if previously set).
	"""
	# prepare query
	sql = "select name, tag, advanced from Subjects where rowid = ?"
	cursor = db.execute(sql, (rowid, ))
	raw = cursor.fetchone()
	
	# parse result
	data = dict()
	if raw is not None:
		data['name'] = raw[0]
		data['tag']  = raw[1]
		if raw[2] is not None:
			data['advanced'] = bool(raw[2])
	return data


def readRowids(db, name: str) -> List[int]:
	"""Return subjects' rowids specified by its `name`."""
	criteria = "%" + name + "%"
	# execute query
	sql = "select rowid from Subjects where name like ?"
	cursor = db.execute(sql, (criteria, ))
	raw = cursor.fetchall()
	
	# parse result
	ids = list()
	for item in raw:
		ids.append(item[0])
	return ids


def rename(db, rowid: int, name: str, tag: str, advanced: bool=None):
	"""Rename the given subject (specified by `rowid`) using the given `name`
	and `tag`. It can optionally be flagged as advanced or not advanced (default
	is not flagged at all).
	"""
	if advanced is not None:
		advanced = int(advanced)
		
	# execute query
	sql = "update Subjects set name = ?, tag = ?, advanced = ? where rowid = ?"
	db.execute(sql, (name, tag, advanced, rowid, ))


def delete(db, rowid: int):
	"""Delete the given subject (specified by `rowid`)."""
	# execute query
	sql = "delete from Subjects where rowid = ?"
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
		create(self.cur, [
			{'name': 'Maths',     'tag': 'Ma', 'advanced': True}, # advanced subject
			{'name': 'Chemistry', 'tag': 'che'},				  # regular subject
			{'name': 'English',   'tag': 'en', 'advanced': False} # basic subject
		])
		
		ids = readAllIds(self.cur)
		self.assertEqual(set(ids), set([1, 2, 3]))
		
		delete(self.cur, 2)
		
		ids = readAllIds(self.cur)
		self.assertEqual(set(ids), set([1, 3]))

	def test_read_subject_data(self):
		create(self.cur, [
			{'name': 'Maths',     'tag': 'Ma', 'advanced': True},
			{'name': 'Chemistry', 'tag': 'che'},
			{'name': 'English',   'tag': 'en', 'advanced': False}
		])
		
		data = readData(self.cur, 3)
		self.assertEqual(data, {'name': 'English', 'tag': 'en', 'advanced': False})
		
		data = readData(self.cur, 1)
		self.assertEqual(data, {'name': 'Maths', 'tag': 'Ma', 'advanced': True})
		
		data = readData(self.cur, 2)
		self.assertEqual(data, {'name': 'Chemistry', 'tag': 'che'})

	def test_search_subjects(self):
		create(self.cur, [
			{'name': 'Maths',   'tag': 'Ma', 'advanced': True},  # advanced course
			{'name': 'Maths',   'tag': 'Ma'},					 # regular maths subject
			{'name': 'Maths',   'tag': 'Ma', 'advanced': False}, # basic course
			{'name': 'English', 'tag': 'en', 'advanced': False}
		])
		
		ids = readRowids(self.cur, 'Maths')
		self.assertEqual(set(ids), set([1, 2, 3]))
		
		ids = readRowids(self.cur, 'ath')
		self.assertEqual(set(ids), set([1, 2, 3]))
		
		ids = readRowids(self.cur, 'Eng')
		self.assertEqual(set(ids), set([4]))
		
		ids = readRowids(self.cur, 'De')
		self.assertEqual(set(ids), set([]))
		
	def test_rename_subject(self):
		create(self.cur, [
			{'name': 'Maths',     'tag': 'Ma', 'advanced': True},
			{'name': 'Chemistry', 'tag': 'che'},
			{'name': 'English',   'tag': 'en', 'advanced': False}
		])
		
		# reset advanced-flag
		rename(self.cur, 1, 'Biology', 'bio')
		data = readData(self.cur, 1)
		self.assertEqual(data, {'name': 'Biology', 'tag': 'bio'})
		
		# set advanced-flag
		rename(self.cur, 1, 'Biology', 'bio', True)
		data = readData(self.cur, 1)
		self.assertEqual(data, {'name': 'Biology', 'tag': 'bio', 'advanced': True})
		
		rename(self.cur, 1, 'Biology', 'bio', False)
		data = readData(self.cur, 1)
		self.assertEqual(data, {'name': 'Biology', 'tag': 'bio', 'advanced': False})
		
		

