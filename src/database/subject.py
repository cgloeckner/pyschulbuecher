# -*- coding: utf-8 -*-

import common

def setup():
	'''
	Build and return sql string for the subjects table.
	'''
	return common.setup('subjects', {
		'name': 'VARCHAR(50) UNIQUE'
	}, {})


def create(name):
	'''
	Build and return sql string for adding a subject.
	'''
	return common.create('subjects', {
		'name': '"%s"' % name
	})


def readNameById(id):
	'''
	Build and return sql string for querying a subject name by id.
	'''
	return common.read('subjects', 'id = %s' % id, ['name'])


def readIdByName(name, attribs=None):
	'''
	Build and return sql string for querying a subject id by name.
	'''
	return common.read('subjects', 'name = %s


