#!/usr/bin/python3
# -*- coding: utf-8 -*-

import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

__author__ = "Christian Glöckner"

import unittest

from db import orm, orga, books, loans, utils
import admin, classes, loans

def register(suite, class_):
	"""Register all testcase methods of the given test case class to the given
	suite
	"""
	for method in dir(class_):
		if method.startswith('test_'):
			suite.addTest(class_(method))

def suite():
	"""Create whole test suite
	"""
	suite = unittest.TestSuite()
	register(suite, orm.Tests)
	register(suite, orga.Tests)
	register(suite, books.Tests)
	register(suite, loans.Tests)
	register(suite, utils.Tests)
	register(suite, admin.Tests)
	register(suite, classes.Tests)
	register(suite, loans.Tests)
	return suite

if __name__ == '__main__':
	orm.db.bind('sqlite', ':memory:', create_db=True)
	orm.db.generate_mapping(create_tables=True)
	
	runner = unittest.TextTestRunner()
	runner.run(suite())
