# -*- coding: utf-8 -*-

def connect(filename):
	from sqlite3 import connect
	
	return connect(filename)


def setup(name, attribs, foreign=dict()):
	'''
	Build and return sql string for CREATE TABLE.
	The table with has the given `name`, hold all attributes given in the
	`attribs` dict and all foreign keys, that are given in the `foreign` dict.
	
	Example:
		setup('books', {
			'title'        : 'varchar(255)',
			'publisher_id' : int,
			'subject_id'   : int
		}, {
			'publisher_id' : 'Publishers'
			'subject_id'   : 'Subjects'
		})
	'''
	
	raw_attribs = ',\n\t'

	raw_foreign = 'FOREIGN KEY ({0}) REFERENCES {1}(id)'

	raw_setup = '''CREATE TABLE {0} (
	id INT NOT NULL,
	{1},
	PRIMARY KEY (id){2}
);'''
	
	# pre-format attributes string
	attr = raw_attribs.join([' '.join([key, attribs[key]]) for key in attribs])
	
	# pre-format foreign key list
	frgn = raw_attribs.join([raw_foreign.format(key, foreign[key]) for key in foreign])
	if len(frgn) > 0:
		frgn = ',\n\t%s' % frgn
	
	# build sql string
	sql = raw_setup.format(name, attr, frgn)

	return sql


def create(name, pairs):
	'''
	Build and return sql string for INSERT INTO.
	The data will be inserted into the `name`d table and is specified by a dict
	of `pairs` with attributes and values.
	
	Example:
		create('books', {
			'title'        : 'Vector geometry',
			'publisher_id' : 17,
			'subject_id'   : 4
		})
	'''
	
	raw_create = 'INSERT INTO {0} ({1}) VALUES ({2});'
	
	# pre-format lists
	keys = ', '.join([key for key in pairs])
	vals = ', '.join([str(pairs[key]) for key in pairs])
	
	# build sql string
	sql = raw_create.format(name, keys, vals)
	
	return sql


def read(name, conditions, attribs=None):
	'''
	Build and return sql string for SELECT using WHERE.
	The data will be queried from the `name`d table using the given `id`.
	The `conditions` list contains pre-formatted WHERE conditions.
	Which data is queried can be specified by the `attribs` list. If `None`
	is provided (default), all attributes are queried.
	
	Example:
		readById('books', 'id = 103')
		readById('books', 'id = 103', ['title', 'subject_id'])
	'''
	
	raw_read = 'SELECT {0} FROM {1} WHERE {2};'
	
	# pre-format attributes list
	attr = '*'
	if attribs is not None:
		attr = ', '.join(attribs)
	
	# build sql string
	sql = raw_read.format(attr, name, conditions)
	
	return sql


# TODO CRUD Create Read Update Delete


# -----------------------------------------------------------------------------

import unittest

class CRUDTest(unittest.TestCase):

	def test_setup_without_foreignkeys(self):
		expect = '''CREATE TABLE subjects (
	id INT NOT NULL,
	name VARCHAR(50) UNIQUE,
	stuff_id INT,
	PRIMARY KEY (id)
);'''
		sql = setup('subjects', {
			'name': 'VARCHAR(50) UNIQUE',
			'stuff_id': 'INT'
		}, {})
		self.assertEqual(sql, expect)
	
	def test_setup_with_foreignkeys(self):
		expect = '''CREATE TABLE subjects (
	id INT NOT NULL,
	name VARCHAR(50) UNIQUE,
	stuff_id INT,
	more_id INT,
	PRIMARY KEY (id),
	FOREIGN KEY (stuff_id) REFERENCES stuff(id),
	FOREIGN KEY (more_id) REFERENCES more(id)
);'''
		sql = setup('subjects', {
			'name': 'VARCHAR(50) UNIQUE',
			'stuff_id': 'INT',
			'more_id': 'INT'
		}, {
			'stuff_id': 'stuff',
			'more_id': 'more'
		})
		self.assertEqual(sql, expect)
	
	def test_create(self):
		expect = 'INSERT INTO subjects (name, stuff_id) VALUES ("maths", 13);'
		sql = create('subjects', {'name': '"maths"', 'stuff_id': 13})
		self.assertEqual(sql, expect)
	
	def test_read_some(self):
		expect = 'SELECT name, more_id FROM subjects WHERE id = 123;'
		sql = read('subjects', 'id = 123', ['name', 'more_id'])
		self.assertEqual(sql, expect)

	def test_read_all(self):
		expect = 'SELECT * FROM subjects WHERE id = 123;'
		sql = read('subjects', 'id = 123')
		self.assertEqual(sql, expect)

if __name__ == '__main__':
	unittest.main()



