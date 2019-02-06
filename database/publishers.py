#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CRUD module for Publishers using prepared statements

Example:
	cur.execute(read, (153,))

SQL-Statement   Paramters
-------------------------	
create          Name
listing			-
search			Name
read            Rowid
update          Name, Rowid
delete          Rowid
"""

__author__ = "Christian Glöckner"

setup = """create table Publishers (
	name varchar(25) unique
);"""

from typing import Iterable, Dict, List

def create(db, names: Iterable[str]):
	"""Create new publishers using the given list of `str` strings."""
	# dump data to list of tuples
	args = list()
	for name in names:
		args.append((name, ))
	
	# execute query
	sql = "insert into Publishers (name) values (?)"
	db.executemany(sql, args)


def readAll(db) -> List[int]:
	"""Returns a full listing of all publishers rowids and names."""
	# execute query
	sql = "select rowid, name from Publishers"
	cursor = db.execute(sql)
	raw = cursor.fetchall()
	
	# parse result
	ret = list()
	for item in raw:
		data = dict()
		data['rowid'] = item[0]
		data['name']  = item[1]
		ret.append(data)
	return ret


def readRowids(db, name: str) -> List[int]:
	"""Return publishers' rowids specified by its `name`."""
	criteria = "%" + name + "%"
	# execute query
	sql = "select rowid from Publishers where name like ?"
	cursor = db.execute(sql, (criteria, ))
	raw = cursor.fetchall()
	
	# parse result
	ids = list()
	for item in raw:
		ids.append(item[0])
	return ids


def rename(db, rowid: int, name: str):
	"""Rename the given publisher (specified by `rowid`) using the given `name`.
	"""
	# execute query
	sql = "update Publishers set name = ? where rowid = ?"
	db.execute(sql, (name, rowid, ))


def delete(db, rowid: int):
	"""Delete the given publisher (specified by `rowid`)."""
	# execute query
	sql = "delete from Publishers where rowid = ?"
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
		create(self.cur, ['Cornelsen', 'Klett', 'Volk und Wissen'])
		
		data = readAll(self.cur)
		self.assertEqual(data, [
			{'rowid': 1, 'name': 'Cornelsen'},
			{'rowid': 2, 'name': 'Klett'},
			{'rowid': 3, 'name': 'Volk und Wissen'}
		])
		
		delete(self.cur, 2)
		
		data = readAll(self.cur)
		self.assertEqual(data, [
			{'rowid': 1, 'name': 'Cornelsen'},
			{'rowid': 3, 'name': 'Volk und Wissen'}
		])
		
	def test_search_publishers(self):
		create(self.cur, ['Cornelsen', 'Klett', 'Volk und Wissen'])
		
		ids = readRowids(self.cur, 'en') # CornelsEN, Volk und WissEN
		self.assertEqual(set(ids), set([1, 3]))
		
		ids = readRowids(self.cur, 'e')
		self.assertEqual(set(ids), set([1, 2, 3]))
		
		ids = readRowids(self.cur, 'tt')
		self.assertEqual(set(ids), set([2]))
		
		ids = readRowids(self.cur, 'mann')
		self.assertEqual(set(ids), set([]))
		
	def test_rename_publishers(self):
		create(self.cur, ['Cornelsen', 'Klett', 'Volk und Wissen'])
		
		rename(self.cur, 3, 'Volk & Wissen')
		data = readAll(self.cur)
		self.assertEqual(data[2]['name'], 'Volk & Wissen')

	def test_unique_name(self):
		create(self.cur, ['Cornelsen', 'Klett', 'Volk und Wissen'])
		
		with self.assertRaises(sqlite3.IntegrityError):
			rename(self.cur, 3, 'Klett')

